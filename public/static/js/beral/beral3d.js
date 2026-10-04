// Beral 3D: loads the rigged GLB, plays and blends its animation clips, and draws it on a transparent canvas.
// This module only knows about the character. The app decides when to call play() and where the canvas sits.
import {
  AnimationMixer, Box3, Clock, Color, DirectionalLight, HemisphereLight, LoopOnce, LoopRepeat, PerspectiveCamera, Scene,
  SRGBColorSpace, Vector3, WebGLRenderer,
} from "three";
import { DRACOLoader } from "three/addons/loaders/DRACOLoader.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { MeshoptDecoder } from "three/addons/libs/meshopt_decoder.module.js";

import { BLINK, EXPRESSIONS, FADE, STATES } from "./animations.js";

const CALM_FPS = 30;
const clipKey = (name) => name.split("|").pop().trim().toLowerCase();

// Load the model and return a controller, or throw when it cannot be shown.
export async function createBeral({ container, modelUrl, decoderPath, maxPixelRatio = 1.75, onState = () => {}, onLost = () => {} }) {
  const gltf = await loadModel(modelUrl, decoderPath);
  const model = gltf.scene;
  if (!gltf.animations.length) throw new Error("The Beral model has no animation clips.");
  let skinned = false;
  model.traverse((node) => {
    if (node.isSkinnedMesh) skinned = true;
    if (node.isMesh) node.frustumCulled = false;
  });
  if (!skinned) throw new Error("The Beral model has no skeleton.");

  const renderer = new WebGLRenderer({ alpha: true, antialias: window.devicePixelRatio < 2, powerPreference: "low-power" });
  renderer.outputColorSpace = SRGBColorSpace;
  renderer.setClearColor(0x000000, 0);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, maxPixelRatio));
  renderer.domElement.className = "beral-canvas";
  container.append(renderer.domElement);

  const scene = new Scene();
  scene.add(model);
  scene.add(new HemisphereLight(0xffffff, 0x3a4060, 1.6));
  const key = new DirectionalLight(0xffffff, 2.2);
  key.position.set(2, 4, 5);
  const rim = new DirectionalLight(new Color(0x9fb4ff), 1.1);
  rim.position.set(-3, 3, -4);
  scene.add(key, rim);

  // Animation clips, matched by name without case or exporter prefixes.
  const mixer = new AnimationMixer(model);
  const clips = new Map(gltf.animations.map((clip) => [clipKey(clip.name), clip]));
  const resolve = (name) => {
    const definition = STATES[name];
    if (!definition) return null;
    const option = definition.options.find((names) => names.every((clip) => clips.has(clip.toLowerCase())));
    return option ? option.map((clip) => clips.get(clip.toLowerCase())) : null;
  };
  const available = () => Object.keys(STATES).filter((name) => resolve(name));

  // Facial morph targets, when the model has them.
  const faces = [];
  model.traverse((node) => {
    if (node.morphTargetDictionary && node.morphTargetInfluences) faces.push(node);
  });
  const morph = (name) => faces.flatMap((mesh) => (name in mesh.morphTargetDictionary ? [[mesh, mesh.morphTargetDictionary[name]]] : []));
  const blinkTargets = morph(BLINK.find((name) => morph(name).length) || "");
  const expressionTargets = new Map();
  let expressionGoal = {};

  // Armour lights that can pulse gently while idle.
  const glows = [];
  model.traverse((node) => {
    for (const material of [node.material].flat().filter(Boolean)) {
      if (material.emissive && material.emissive.getHex() !== 0 && !glows.includes(material)) {
        material.userData.baseGlow = material.emissiveIntensity;
        glows.push(material);
      }
    }
  });

  let current = null;
  let state = null;
  let queue = [];
  let returnTo = "idle";
  const clock = new Clock();
  let frameId = 0;
  let active = true;
  let elapsed = 0;
  let pending = 0;
  let nextBlink = 2 + Math.random() * 3;
  let blinkTime = -1;

  // Ease the face towards a named expression, or back to neutral for null.
  function setExpression(name) {
    expressionGoal = {};
    for (const [morphName, weight] of Object.entries(EXPRESSIONS[name] || {})) {
      if (!expressionTargets.has(morphName)) expressionTargets.set(morphName, morph(morphName));
      if (expressionTargets.get(morphName).length) expressionGoal[morphName] = weight;
    }
    for (const morphName of expressionTargets.keys()) expressionGoal[morphName] ??= 0;
  }

  function start(clip, loop) {
    const action = mixer.clipAction(clip);
    action.reset();
    action.setLoop(loop ? LoopRepeat : LoopOnce, loop ? Infinity : 1);
    action.clampWhenFinished = !loop;
    action.enabled = true;
    action.setEffectiveTimeScale(1);
    action.setEffectiveWeight(1);
    if (current && current !== action) action.crossFadeFrom(current, FADE, true);
    else if (!current) action.fadeIn(FADE);
    action.play();
    current = action;
  }

  // Play a state by name. Returns false when the model has no clip for it, so nothing is faked.
  function play(name) {
    const definition = STATES[name];
    if (definition && definition.loop && name === state && current && current.isRunning()) return true;
    const sequence = resolve(name);
    if (!sequence) {
      console.warn(`Beral has no animation for "${name}".`);
      return false;
    }
    state = name;
    returnTo = definition.loop ? name : "idle";
    queue = sequence.slice(1);
    start(sequence[0], Boolean(definition.loop));
    setExpression(definition.expression);
    onState(name);
    wake();
    return true;
  }

  mixer.addEventListener("finished", (event) => {
    if (event.action !== current) return;
    if (queue.length) start(queue.shift(), false);
    else play(returnTo);
  });

  // Start in the resting state, then frame that pose with room above the head for jumps and beside it for waving arms.
  play(resolve("idle") ? "idle" : available()[0]);
  mixer.update(0);
  model.updateMatrixWorld(true);
  const box = new Box3().setFromObject(model, true);
  const size = box.getSize(new Vector3());
  const center = box.getCenter(new Vector3());
  const camera = new PerspectiveCamera(28, 1, size.y / 100, size.y * 100);
  const frame = () => {
    const width = Math.max(container.clientWidth, 1);
    const height = Math.max(container.clientHeight, 1);
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    const half = Math.tan((camera.fov * Math.PI) / 360);
    const distance = Math.max((size.y * 1.32) / 2 / half, (size.x * 1.6) / 2 / half / camera.aspect) + size.z / 2;
    camera.position.set(center.x, center.y + size.y * 0.08, center.z + distance);
    camera.lookAt(center.x, center.y + size.y * 0.08, center.z);
    camera.updateProjectionMatrix();
  };
  frame();

  // Rendering runs only while the canvas is shown and the tab is open, at a lower rate while calm.
  function tick() {
    frameId = 0;
    if (!active || document.hidden) return;
    frameId = requestAnimationFrame(tick);
    pending += Math.min(clock.getDelta(), 0.1);
    const calm = state === "idle" || state === "thinking";
    if (calm && pending < 1 / CALM_FPS) return;
    const step = pending;
    pending = 0;
    elapsed += step;
    mixer.update(step);
    for (const [morphName, goal] of Object.entries(expressionGoal)) {
      for (const [mesh, index] of expressionTargets.get(morphName) || []) {
        mesh.morphTargetInfluences[index] += (goal - mesh.morphTargetInfluences[index]) * Math.min(step * 6, 1);
      }
    }
    if (blinkTargets.length) {
      if (elapsed > nextBlink) {
        blinkTime = 0;
        nextBlink = elapsed + 2.5 + Math.random() * 4;
      }
      if (blinkTime >= 0) {
        blinkTime += step;
        const closed = blinkTime < 0.09 ? blinkTime / 0.09 : Math.max(0, 1 - (blinkTime - 0.09) / 0.12);
        for (const [mesh, index] of blinkTargets) mesh.morphTargetInfluences[index] = closed;
        if (blinkTime > 0.21) blinkTime = -1;
      }
    }
    for (const material of glows) {
      material.emissiveIntensity = material.userData.baseGlow * (calm ? 1 + 0.15 * Math.sin(elapsed * 2) : 1);
    }
    renderer.render(scene, camera);
  }

  function wake() {
    if (!frameId && active && !document.hidden) {
      clock.getDelta();
      frameId = requestAnimationFrame(tick);
    }
  }

  function sleep() {
    if (frameId) cancelAnimationFrame(frameId);
    frameId = 0;
  }

  const onVisibility = () => (document.hidden ? sleep() : wake());
  document.addEventListener("visibilitychange", onVisibility);
  const resizer = new ResizeObserver(() => {
    frame();
    renderer.render(scene, camera);
  });
  resizer.observe(container);
  renderer.domElement.addEventListener("webglcontextlost", (event) => {
    event.preventDefault();
    sleep();
    onLost();
  });

  // Stop drawing while Beral is hidden, and resume when shown again.
  function setActive(on) {
    active = on;
    if (on) wake();
    else sleep();
  }

  // Free the GPU memory used by the model.
  function dispose() {
    setActive(false);
    document.removeEventListener("visibilitychange", onVisibility);
    resizer.disconnect();
    mixer.stopAllAction();
    mixer.uncacheRoot(model);
    model.traverse((node) => {
      if (node.geometry) node.geometry.dispose();
      for (const material of [node.material].flat().filter(Boolean)) {
        for (const value of Object.values(material)) if (value && value.isTexture) value.dispose();
        material.dispose();
      }
    });
    renderer.dispose();
    renderer.domElement.remove();
  }

  // Describe the model, for the admin preview page and for checks.
  const clipNames = () => gltf.animations.map((clip) => clip.name);
  const boneNames = () => {
    const names = [];
    model.traverse((node) => node.isBone && names.push(node.name));
    return names;
  };
  const morphNames = () => [...new Set(faces.flatMap((mesh) => Object.keys(mesh.morphTargetDictionary)))];

  return {
    play, setActive, dispose, available, clipNames, boneNames, morphNames, setExpression,
    get state() { return state; },
    get action() { return current; },
    get model() { return model; },
    get frames() { return renderer.info.render.frame; },
  };
}

// Read the GLB, with support for Draco and meshopt compressed files.
function loadModel(url, decoderPath) {
  const loader = new GLTFLoader();
  if (decoderPath) {
    const draco = new DRACOLoader();
    draco.setDecoderPath(decoderPath);
    loader.setDRACOLoader(draco);
  }
  loader.setMeshoptDecoder(MeshoptDecoder);
  return loader.loadAsync(url);
}
