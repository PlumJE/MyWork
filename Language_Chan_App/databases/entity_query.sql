CREATE TABLE IF NOT EXISTS CharaInfo(
    charanum INT NOT NULL UNIQUE,
    name TEXT,
    profileimg TEXT,
    fullimg TEXT,
    fightimg TEXT,
    atkexp TEXT,
    dfsxep TEXT,
    PRIMARY KEY(charanum)
);

CREATE TABLE IF NOT EXISTS EnemyInfo(
    enemynum INT NOT NULL UNIQUE,
    name TEXT,
    profileimg TEXT,
    fightimg TEXT,
    atk INT,
    dfs INT,
    PRIMARY KEY(enemynum)
);

UPDATE CharaInfo SET profileimg="english_chan.jpg", fullimg="english_chan.jpg", fightimg="english_chan.jpg" WHERE charanum=1;
UPDATE CharaInfo SET profileimg="chinese_chan.jpg", fullimg="chinese_chan.jpg", fightimg="chinese_chan.jpg" WHERE charanum=2;