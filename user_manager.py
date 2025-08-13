# user_manager.py
import pandas as pd
import os
from datetime import datetime

class UserManager:
    def __init__(self):
        self.csv_path = 'data/users.csv'
        self.ensure_csv_exists()

    def ensure_csv_exists(self):
        """CSV 파일이 없으면 생성"""
        if not os.path.exists(self.csv_path):
            os.makedirs('data', exist_ok=True)
            empty_df = pd.DataFrame(columns=['user_id', 'username', 'password', 'created_at'])
            empty_df.to_csv(self.csv_path, index=False, encoding='utf-8')

    def load_users(self):
        """사용자 데이터 로드"""
        try:
            return pd.read_csv(self.csv_path, encoding='utf-8')
        except:
            return pd.DataFrame(columns=['user_id', 'username', 'password', 'created_at'])

    def save_users(self, df):
        """사용자 데이터 저장"""
        df.to_csv(self.csv_path, index=False, encoding='utf-8')

    def create_user(self, username, password):
        """새 사용자 생성"""
        users_df = self.load_users()

        # 중복 사용자명 체크
        if username in users_df['username'].values:
            return False, "이미 존재하는 사용자명입니다."

        # 새 사용자 ID 생성
        user_count = len(users_df)
        new_user_id = f"user_{user_count + 1:03d}"  # user_001, user_002...

        # 새 사용자 데이터
        new_user = {
            'user_id': new_user_id,
            'username': username,
            'password': password,
            'created_at': datetime.now().strftime('%Y-%m-%d')
        }

        # DataFrame에 추가
        new_row = pd.DataFrame([new_user])
        users_df = pd.concat([users_df, new_row], ignore_index=True)

        # 저장
        self.save_users(users_df)
        return True, "회원가입이 완료되었습니다!"

    def login_user(self, username, password):
        """사용자 로그인 검증"""
        users_df = self.load_users()

        # 사용자 찾기
        user_data = users_df[
            (users_df['username'] == username) &
            (users_df['password'] == password)
        ]

        if len(user_data) == 1:
            user_info = user_data.iloc[0].to_dict()
            return True, user_info
        else:
            return False, None

    def get_user_count(self):
        """총 사용자 수 반환"""
        users_df = self.load_users()
        return len(users_df)

