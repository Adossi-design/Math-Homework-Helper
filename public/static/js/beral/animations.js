// Beral's behaviours. Edit this file to add a new state such as "confused" or "pointing".
//
// Each state lists one or more options. An option is a list of clip names from the GLB that play one
// after another. The first option whose clips all exist in the model is used, so a model that has a
// dedicated "Celebrate" clip uses it, while a model with only "Jump" and "Turn" builds the same behaviour
// from those. Clip names are matched without case and without exporter prefixes like "Armature|".
//
// loop: true keeps the state running until another state is played (idle, thinking).
// Other states play once and then fade back to idle.
// expression names a facial expression from EXPRESSIONS, used when the model has those morph targets.

export const STATES = {
  idle: { loop: true, options: [["Idle"]], expression: null },
  thinking: { loop: true, options: [["Thinking"]], expression: "thoughtful" },
  welcome: { options: [["Welcome"], ["Wave"]], expression: "smile" },
  success: { options: [["Success"], ["ThumbsUp"], ["Yes"]], expression: "smile" },
  celebrate: { options: [["Celebrate"], ["Jump", "Turn"], ["Jump"]], expression: "joy" },
  encourage: { options: [["Encourage"], ["ThumbsUp"], ["Yes"]], expression: "smile" },
};

// Facial expressions as morph target names with a weight. Any name the model does not have is skipped.
export const EXPRESSIONS = {
  smile: { Smile: 0.8, Happy: 0.8, mouthSmile: 0.8, BrowsUp: 0.3 },
  joy: { Smile: 1, Happy: 1, mouthSmile: 1, MouthOpen: 0.5, BrowsUp: 0.5 },
  thoughtful: { Thinking: 0.8, Thoughtful: 0.8, BrowsDown: 0.4, browInnerUp: 0.5, MouthSide: 0.4 },
};

// Morph targets used for blinking, tried in this order.
export const BLINK = ["Blink", "EyesClosed", "eyeBlink", "eyesClosed"];

// Seconds used to blend from one state into the next.
export const FADE = 0.4;
