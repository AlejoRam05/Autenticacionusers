import bcrypt

class HashMethod:
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashea la contraseña utilizando bcrypt.
        """
        salt = bcrypt.gensalt()  # Genera un salt aleatorio
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        Verifica si la contraseña coincide con el hash almacenado.
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception as e:
            # Manejo de errores si ocurre algún problema con el hashing
            raise ValueError("Error al verificar la contraseña: " + str(e))
