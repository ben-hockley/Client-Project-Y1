CREATE TABLE IF NOT EXISTS `QuizHistory` (
  `ID`		INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `quizName`		TEXT NOT NULL,
  'genre'   TEXT NOT NULL,   
  'author'    TEXT NOT NULL
);

-- Look at the quotes They are different on each line.  See https://sqlite.org/lang_keywords.html
INSERT INTO 'QuizHistory'('quizName','genre', 'author' ) VALUES ('First Aid','Health+Safety','Ben');
INSERT INTO `QuizHistory`(`quizName`,`genre`, `author` ) VALUES ('Internet Safety','Health+Safety','Freddie');
INSERT INTO "QuizHistory"("quizName","genre", "author" ) VALUES ('Team Building','Social','Alex');
INSERT INTO QuizHistory (quizName,genre, author) VALUES ('Assessment 1','Tests','Sam');