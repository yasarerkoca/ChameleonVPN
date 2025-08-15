from sqlalchemy.orm import Session
from app.models.user.user_referral_rewards import UserReferralReward
from app.schemas.user.user_meta import ReferralRewardCreate
from typing import List


def create_referral_reward(db: Session, reward_data: ReferralRewardCreate) -> UserReferralReward:
    reward = UserReferralReward(**reward_data.dict())
    db.add(reward)
    db.commit()
    db.refresh(reward)
    return reward


def get_rewards_by_user(db: Session, user_id: int) -> List[UserReferralReward]:
    return db.query(UserReferralReward).filter(UserReferralReward.user_id == user_id).all()


def get_rewards_by_referrer(db: Session, referrer_id: int) -> List[UserReferralReward]:
    return db.query(UserReferralReward).filter(UserReferralReward.referrer_id == referrer_id).all()
