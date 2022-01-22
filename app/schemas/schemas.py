from pydantic import BaseModel, Field
from typing import List, Optional


class Link(BaseModel):
    href: str
    target: str = Field('_blank')


class PreviewImage(BaseModel):
    src: str = Field('noimage.png')
    border: int = Field(0)
    width: int = Field(50)
    height: int = Field(50)
    alt: str = Field('')
    loading: str = Field('lazy')


# URLのプレフィックス結合どこで行うか...
class ThreadPreview(BaseModel):
    id: int = Field(0)
    title: str = Field('スレタイ')
    resNum: int = Field(0)
    a: Link = Field({'href': 'http://img.2chan.net/b/res/0.htm'})
    img: Optional[PreviewImage] = None


class Catalog(BaseModel):
    id: int = Field(0)
    items: List[ThreadPreview] = Field(0)


class Comment(BaseModel):
    id: int
    name: str = Field('名無しさん')
    # TODO: replace str with date
    date: str = Field('1900-01-01 00:00:00')
    rate: int
    src: str = Field('noimage.png')
    content: str = Field('This is a comment.')


class Thread(BaseModel):
    id: int = Field(0)
    items: List[Comment] = Field([])
