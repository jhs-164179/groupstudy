use db_kbk;

create table person_table( -- 사람의 정보를 저장
    personID INT PRIMARY KEY, -- 학번
    personName VARCHAR(20), -- 사람 이름
    personPassword VARCHAR(20) -- 비밀번호
);

create table room_table( -- 방 정보를 저장
    roomID INT PRIMARY KEY -- 방 번호
);

create table room_person( -- 사람마다 권한받은 방의 정보 저장
    Id INT AUTO_INCREMENT PRIMARY KEY, -- 일련번호 (대리키)
    personID INT, -- 학번
    roomId INT, -- 룸 번호(학번에 권한 부여된 룸 번호 -> sql 작성자가 직접 추가 할 듯)
    FOREIGN KEY (personID) REFERENCES person_table(personID),
    FOREIGN KEY (roomID) REFERENCES room_table(roomID)
);
-- 이미지 저장 시
create table results( -- 탐지 결과 저장
    Id INT AUTO_INCREMENT PRIMARY KEY, -- 일련번호 (대리키)
    fileName VARCHAR(50),
    roomId INT,
    images mediumblob,
    FOREIGN KEY (roomId) REFERENCES room_table(roomID)
);

-- 이미지 저장말고 결과만 저장시
create table results(
    classId INT PRIMARY KEY,
    X DOUBLE,
    Y DOUBLE,
    width double,
    height double
);

-- room_person에 직접 학번에 권한 부여된 방 삽입하는 쿼리문
INSERT INTO room_person(personID, roomID)
VALUE( , );