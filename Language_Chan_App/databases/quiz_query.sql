CREATE TABLE IF NOT EXISTS ClassInfo(
    classnum INT NOT NULL UNIQUE,
    language TEXT,
    bgimg TEXT,
    PRIMARY KEY(classnum)
);
CREATE TABLE IF NOT EXISTS QuizInfo(
    classnum INT,
    quiznum INT,
    lvl INT,
    x_cor FLOAT,
    y_cor FLOAT,
    btnimg TEXT,
    bgimg TEXT,
    FOREIGN KEY(classnum) REFERENCES ClassInfo(classnum)
);

INSERT INTO ClassInfo(classnum, language, bgimg) VALUES(1, 'English', 'english_class_bg.jpg');
INSERT INTO ClassInfo(classnum, language, bgimg) VALUES(2, 'Chinese', 'chinese_class_bg.jpg');