from pydantic import BaseModel, Field
from typing import List, Optional


class Link(BaseModel):
    href: str = Field('http://img.2chan.net/b/res/0.htm')
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
    a: Link = Field(Link())
    img: Optional[PreviewImage] = None


class Catalog(BaseModel):
    id: int = Field(0)
    items: List[ThreadPreview] = Field(0)


class CommentImage(BaseModel):
    src: Optional[str] = Field(None)


class Comment(BaseModel):
    order: int = Field(0)
    title: str = Field('無題')
    name: str = Field('としあき')
    # TODO: replace str with date
    date: str = Field('1900-01-01 00:00:00')

    rate: Optional[int] = Field(0)
    body: str = Field('This is a comment.')
    img: CommentImage = Field(CommentImage())


class Thread(BaseModel):
    # id: int = Field(0)
    title: str = Field('スレタイ')
    items: List[Comment] = Field([])
