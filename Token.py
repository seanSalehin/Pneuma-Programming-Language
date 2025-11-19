from enum import Enum
from typing import Any

class TokenType(Enum):
    #End of file token
    EOF = "EOF"

    #Lexor Error
    ILLEGAL = "ILLEGAL"
    

    #Data Types
    IDENT = "IDENT"
    INT = "INT"
    FLOAT = "FLOAT"
    


    #Arithmatic Symbols
    PLUS = "PLUS"
    MINUS = "MINUS"
    ASTERISK = "ASTERISK"
    SLASH = "SLASH"
    POW = "POW"
    MODULUS = "MODULUS"


    #Assignment Symbols
    EQ = "EQ"


    #Symbols
    COLON = "COLON"
    SEMICOLON = "SEMICOLON"
    LEFTPARENTHESES = "LEFTPARENTHESES"
    RIGHTPARENTHESES="RIGHTPARENTHESES"
    ARROW = "ARROW"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"


    #Syntax - Keywords
    LET = "LET"
    ACT = "ACT"
    RETURN = "RETURN"

    #Syntax - Typing
    TYPE = "TYPE"



class Token:
    def __init__(self, type, literal, line_number, position):
        self.type=type
        self.literal=literal
        self.line_number=line_number
        self.position=position
        
    #error
    def __str__(self):
        return f"Token[{self.type}:{self.literal}:Line{self.line_number}:Position{self.position}]"
        
    #representing
    def __repr__(self):
        return str(self)
            

KEYWORDS: dict[str, TokenType] = {
    "let":TokenType.LET,
    "act":TokenType.ACT,
    "return":TokenType.RETURN

}

ALT_KEYWORDS: dict[str, TokenType]={
    "mark": TokenType.LET,
    "=": TokenType.EQ,
    ";" : TokenType.SEMICOLON,
    "act":TokenType.ACT,
    "return":TokenType.RETURN,
    "=>": TokenType.ARROW
}

TYPE_KEYWORDS: list[str] = ["int", "float"]

def lookup_ident(ident:str) -> TokenType:
    tt: TokenType | None = KEYWORDS.get(ident)
    if tt is not None:
        return tt
    tt: TokenType|None = ALT_KEYWORDS.get(ident)
    if tt is not None:
        return tt

    if ident in TYPE_KEYWORDS:
        return TokenType.TYPE
    
    return TokenType.IDENT