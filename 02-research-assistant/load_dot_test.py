import dotenv
import os

loaded = dotenv.load_dotenv()
print(f"Loaded .env from: {loaded}")

env_path = dotenv.find_dotenv()
print(f"Found .env at: {env_path}")

# 실제 값 확인 (중요!)
serper_key = os.getenv('SERPER_API_KEY')
print(f"SERPER_API_KEY loaded: {'YES (' + serper_key[:10] + '...)' if serper_key else 'NO - NOT FOUND'}")