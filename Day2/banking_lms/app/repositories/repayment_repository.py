from sqlalchemy.orm import Session
from app.models.repayment import Repayment


class RepaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_repayment(self, repayment_data: dict):
        new_repayment = Repayment(**repayment_data)
        self.db.add(new_repayment)
        self.db.commit()
        self.db.refresh(new_repayment)
        return new_repayment

    def get_repayment_by_id(self, repayment_id: int) -> Repayment:
        return self.db.query(Repayment).filter(Repayment.id == repayment_id).first()

    def get_repayments_by_application(self, application_id: int, skip: int = 0, limit: int = 10):
        return self.db.query(Repayment).filter(
            Repayment.loan_application_id == application_id
        ).offset(skip).limit(limit).all()

    def get_total_repaid(self, application_id: int) -> float:
        """Calculate total amount repaid for a loan application"""
        result = self.db.query(
            __import__('sqlalchemy').func.sum(Repayment.amount_paid)
        ).filter(Repayment.loan_application_id == application_id).scalar()
        return result or 0.0

    def update_repayment(self, repayment_id: int, repayment_data: dict) -> Repayment:
        repayment = self.get_repayment_by_id(repayment_id)
        if not repayment:
            return None
        for key, value in repayment_data.items():
            if value is not None:
                setattr(repayment, key, value)
        self.db.commit()
        self.db.refresh(repayment)
        return repayment

    def count_repayments(self, application_id: int) -> int:
        return self.db.query(Repayment).filter(
            Repayment.loan_application_id == application_id
        ).count()
