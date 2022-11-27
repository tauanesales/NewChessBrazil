class CastlingRights:

    def __init__(self,whiteKingSide: bool, whiteQueenSide: bool ,blackKingSide: bool, blackQueenSide: bool) -> None:
        self.whiteKingSide = whiteKingSide
        self.whiteQueenSide = whiteQueenSide
        self.blackKingSide = blackKingSide
        self.blackQueenSide = blackQueenSide
    
    def __repr__(self) -> str:
        return f"({self.whiteKingSide},{self.whiteQueenSide},{self.blackKingSide},{self.blackQueenSide})"