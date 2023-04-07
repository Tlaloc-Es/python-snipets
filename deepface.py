from dataclasses import dataclass
from typing import List, Tuple
from numpy import ndarray
from mtcnn import MTCNN

from typing import Tuple
from PIL import Image
from numpy import ndarray, asarray


def resize_image(image: ndarray, required_size: Tuple[int]) -> ndarray:
    image = Image.fromarray(image)
    image = image.resize(required_size)
    image = asarray(image)
    return image


def extract_box_from_image(img: ndarray, x1: int, y1: int, width: int, height: int):
    x2, y2 = x1 + width, y1 + height
    face = img[y1:y2, x1:x2]
    return face


@dataclass
class Keypoints:
    left_eye: Tuple[int]
    right_eye: Tuple[int]
    nose: Tuple[int]
    mouth_left: Tuple[int]
    mouth_right: Tuple[int]


@dataclass
class FaceDetected:
    box: List[int]
    confidence: float
    keypoints: Keypoints


@dataclass
class FacesDetected:
    faces: List[FaceDetected]

    def __next__(self) -> FaceDetected:
        for face in self.faces:
            yield face


@dataclass
class FaceImgWihtKeypoints:
    face: ndarray
    keypoints: Keypoints


def detect_faces_mtcnn(picture) -> FacesDetected:
    detector = MTCNN()
    results = detector.detect_faces(picture)
    return results


def extract_face(
    full_picture: ndarray,
    face_detected: FaceDetected,
    required_size: Tuple[int] = (224, 224),
) -> ndarray:
    x1, y1, width, height = face_detected["box"]
    face_image = extract_box_from_image(full_picture, x1, y1, width, height)
    face_image = resize_image(face_image, required_size)
    return face_image


def get_img_faces(picture) -> List[ndarray]:
    picture = picture[..., :3]
    facesDetected = detect_faces_mtcnn(picture)
    faces = []
    for faceDetected in facesDetected:
        faces.append(extract_face(picture, faceDetected))
    return faces


def get_img_faces_with_keypoints(picture) -> List[FaceImgWihtKeypoints]:
    picture = picture[..., :3]
    facesDetected = detect_faces_mtcnn(picture)
    faces = []
    for faceDetected in facesDetected:
        faces.append(
            FaceImgWihtKeypoints(
                face=extract_face(picture, faceDetected),
                keypoints=faceDetected["keypoints"],
            )
        )
    return faces
