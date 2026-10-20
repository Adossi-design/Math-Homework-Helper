"""Removing a user's data, shared by the settings page and the admin dashboard."""
from sqlalchemy import delete, inspect, select, text

from .extensions import db
from .images import delete_image
from .models import ChapterAttempt, EmailLog, ExerciseResult, LoginAttempt, Solution, TutorQuestion


def remove_solutions(user):
    """Delete every solution and stored photo for a user."""
    for solution in db.session.scalars(select(Solution).where(Solution.user_id == user.id)).all():
        delete_image(solution.image_name)
        db.session.delete(solution)


def delete_user(user):
    """Delete an account with its solutions, photos, progress and email records."""
    remove_solutions(user)
    if "assignment_completion" in inspect(db.engine).get_table_names():
        # Rows left from the retired assignments feature would otherwise block the delete.
        db.session.execute(text("DELETE FROM assignment_completion WHERE user_id = :user"), {"user": user.id})
    for model in (ExerciseResult, ChapterAttempt, TutorQuestion):
        db.session.execute(delete(model).where(model.user_id == user.id))
    db.session.execute(delete(EmailLog).where(EmailLog.email == user.email))
    db.session.execute(delete(LoginAttempt).where(LoginAttempt.email == user.email))
    db.session.delete(user)
