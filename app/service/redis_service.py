import redis
from flask import current_app, has_app_context

class RedisTokenService:
    """Service for managing JWT token blacklist in Redis"""
    
    def __init__(self):
        self.redis_client = None
        self._initialized = False
    
    def _init_redis(self):
        """Initialize Redis connection - safe to call even without app context"""
        if self._initialized:
            return
        
        self._initialized = True
        
        # Don't try to connect if no app context
        if not has_app_context():
            return
        
        try:
            self.redis_client = redis.StrictRedis(
                host=current_app.config.get('REDIS_HOST', 'localhost'),
                port=current_app.config.get('REDIS_PORT', 6379),
                db=current_app.config.get('REDIS_BLACKLIST_DB', 0),
                password=current_app.config.get('REDIS_PASSWORD', None),
                decode_responses=True
            )
            self.redis_client.ping()
        except Exception as e:
            print(f"Redis connection warning: {e}")
            self.redis_client = None
    
    def _ensure_redis(self):
        """Ensure Redis is initialized before operations"""
        self._init_redis()
        return self.redis_client is not None
    
    def add_to_blacklist(self, jti: str, expires_in_seconds: int) -> bool:
        """Add a JWT to the blacklist."""
        if not self._ensure_redis():
            return False
        
        try:
            self.redis_client.setex(f"blacklist:{jti}", expires_in_seconds, "revoked")
            return True
        except Exception:
            return False
    
    def is_blacklisted(self, jti: str) -> bool:
        """Check if a JWT is in the blacklist."""
        if not self._ensure_redis():
            return False
        
        try:
            return self.redis_client.exists(f"blacklist:{jti}") > 0
        except Exception:
            return False
    
    def revoke_all_user_tokens(self, user_id: int) -> bool:
        """Revoke all tokens for a specific user."""
        if not self._ensure_redis():
            return False
        
        try:
            import time
            self.redis_client.setex(f"user_revoked:{user_id}", 86400 * 7, str(int(time.time())))
            return True
        except Exception:
            return False
    
    def get_redis_health(self) -> dict:
        """Check Redis connection health."""
        self._init_redis()
        
        if not self.redis_client:
            return {"status": "disconnected"}
        
        try:
            self.redis_client.ping()
            return {"status": "healthy"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}


redis_token_service = RedisTokenService()
    
    
            