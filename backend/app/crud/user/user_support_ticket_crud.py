from sqlalchemy.orm import Session
from app.models.user.user_support_tickets import UserSupportTicket
from app.schemas.user.user_meta import SupportTicketCreate
from typing import List


def create_support_ticket(db: Session, ticket_data: SupportTicketCreate) -> UserSupportTicket:
    ticket = UserSupportTicket(**ticket_data.dict())
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def get_tickets_by_user(db: Session, user_id: int) -> List[UserSupportTicket]:
    return db.query(UserSupportTicket).filter(UserSupportTicket.user_id == user_id).order_by(
        UserSupportTicket.created_at.desc()
    ).all()


def get_ticket_by_id(db: Session, ticket_id: int) -> UserSupportTicket | None:
    return db.query(UserSupportTicket).filter(UserSupportTicket.id == ticket_id).first()


def update_ticket_status(db: Session, ticket_id: int, new_status: str) -> UserSupportTicket | None:
    ticket = get_ticket_by_id(db, ticket_id)
    if not ticket:
        return None
    ticket.status = new_status
    db.commit()
    db.refresh(ticket)
    return ticket
