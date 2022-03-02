from pydantic import BaseModel, Field
from typing import List, Optional


class Image(BaseModel):
    src: str = Field('http://img.2chan.net/b/thumb/00000.jpg')
    width: int = Field(50)
    height: int = Field(50)
    alt: str = Field('')


# URLのプレフィックス結合どこで行うか...
class ThreadPreview(BaseModel):
    id: int = Field(0)
    title: str = Field('スレタイ')
    resNum: int = Field(0)
    # href: Optional[str] = Field(None)
    img: Optional[Image] = Field(None)


class Catalog(BaseModel):
    items: List[ThreadPreview] = Field([])


class Comment(BaseModel):
    order: int = Field(0)
    title: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    # TODO: replace str with date
    date: str = Field('00/01/01(土)00:00:00')
    no: str = Field('No.111111111')
    sod: Optional[int] = Field(None)
    body: str = Field('This is a comment.')
    href: Optional[str] = Field(None)  # 元画像へのリンク
    img: Optional[Image] = Field(None)


class Thread(BaseModel):
    items: List[Comment] = Field([])


class Board(BaseModel):
    name: str = Field('')
    href: str = Field('')

class Menu(BaseModel):
    items: List[Board] = Field([])
