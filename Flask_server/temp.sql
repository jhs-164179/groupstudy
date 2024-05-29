CREATE TABLE images
(
  imageid        INT AUTO_INCREMENT PRIMARY KEY,    -- 이미지 식별 ID
  imagedata        VARCHAR(255)    -- 이미지 데이터(mysql 스트림 변환?????, VARCHAR이 맞는지 고민)
);

CREATE TABLE image_path (
    imagepathid INT AUTO_INCREMENT PRIMARY KEY,
    imagepathdata VARCHAR(255) NOT NULL
);