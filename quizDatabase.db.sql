DROP TABLE "Answers";
DROP TABLE "Questions";
DROP TABLE "Messages";
DROP TABLE "Players";
DROP TABLE "Mood";
DROP TABLE "Quiz";
DROP TABLE "User";


CREATE TABLE IF NOT EXISTS "User" ("UserID" SERIAL PRIMARY KEY, "Username" TEXT NOT NULL, "FirstName" TEXT NOT NULL, "SurName" TEXT NOT NULL, "Password" TEXT, "Admin" TEXT NOT NULL DEFAULT 'N', "Mood" INT NOT NULL DEFAULT 2, "SecurityQuestion" TEXT, "SecurityAnswer" TEXT);

CREATE TABLE IF NOT EXISTS "Quiz" ("QuizID" SERIAL PRIMARY KEY, "QuizName" TEXT NOT NULL, "UserID" INTEGER NOT NULL, "QuizKey" TEXT);

CREATE TABLE IF NOT EXISTS "Questions" ("QuestionID" SERIAL PRIMARY KEY, "Question" TEXT NOT NULL, "QuizID" INTEGER NOT NULL, "Points" INTEGER NOT NULL);

CREATE TABLE IF NOT EXISTS "Answers" ("AnswerID" SERIAL PRIMARY KEY, "QuestionID" INTEGER NOT NULL, "Answer" TEXT NOT NULL, "IsTrue" TEXT NOT NULL DEFAULT 'F');

CREATE TABLE IF NOT EXISTS "Players" ("PlayerID" SERIAL PRIMARY KEY, "UserID" INTEGER NOT NULL, "Points" INTEGER NOT NULL, "QuizID" INTEGER NOT NULL);

CREATE TABLE IF NOT EXISTS "Mood" ("MoodID" SERIAL PRIMARY KEY, "QuizID" INTEGER NOT NULL, "UserID" INTEGER NOT NULL, "MoodBefore" INTEGER NOT NULL, "MoodAfter" INTEGER NOT NULL);

CREATE TABLE IF NOT EXISTS "Messages" ("MessageID" SERIAL PRIMARY KEY, "QuizID" INTEGER NOT NULL, "UserID" INTEGER NOT NULL, "Message" TEXT, "Time" TEXT, "Date" TEXT);

INSERT INTO "User" ("Username", "FirstName", "SurName", "Password", "Admin", "Mood", "SecurityQuestion", "SecurityAnswer") VALUES ('Raw Pigeon Muscle','Sam','Carter','9f91df00f140105d69c31f25db8fafe5','Y',4,'In what city were you born?','NULL');
INSERT INTO "User" ("Username", "FirstName", "SurName", "Password", "Admin", "Mood", "SecurityQuestion", "SecurityAnswer") VALUES ('sadas','Alex','Ste','60ca9f395404c9c77b4b401c004fa5db','N',2,NULL,NULL);
INSERT INTO "User" ("Username", "FirstName", "SurName", "Password", "Admin", "Mood", "SecurityQuestion", "SecurityAnswer") VALUES ('AlexTARDIS','Alexander','Stephens','df3212b4f61097140c03e7683249f038','N',3,NULL,NULL);
INSERT INTO "User" ("Username", "FirstName", "SurName", "Password", "Admin", "Mood", "SecurityQuestion", "SecurityAnswer") VALUES ('McFreddie','Freddie','Mckay','63d48cdc6ed50e7b47df2b83a4294db0','N',0,NULL,NULL);
INSERT INTO "User" ("Username", "FirstName", "SurName", "Password", "Admin", "Mood", "SecurityQuestion", "SecurityAnswer") VALUES ('McFreddie2','Freddie','Mckay','d8ee16910adf7579dfd4ffe6b228bd7b','N',2,NULL,NULL);
INSERT INTO "User" ("Username", "FirstName", "SurName", "Password", "Admin", "Mood", "SecurityQuestion", "SecurityAnswer") VALUES ('Cooked Pigeon Muscle','Sam','Carter','9f91df00f140105d69c31f25db8fafe5','N',0,NULL,NULL);
INSERT INTO "User" ("Username", "FirstName", "SurName", "Password", "Admin", "Mood", "SecurityQuestion", "SecurityAnswer") VALUES ('runnori_oraltree4','Jess','Harris','e746505afb4afe2fb5eed8b8350ab017','N',4,'',NULL);
INSERT INTO "User" ("Username", "FirstName", "SurName", "Password", "Admin", "Mood", "SecurityQuestion", "SecurityAnswer") VALUES ('ben2','Ben','H','4faa802e8cbd0569f4351bf578c4bf6b','N',2,'In what city were you born?','Cardiff');
INSERT INTO "User" ("Username", "FirstName", "SurName", "Password", "Admin", "Mood", "SecurityQuestion", "SecurityAnswer") VALUES ('benhswfc','Ben','Hockley','9fb40a358dfa9572193fe94ac161f0eb','N',4,'What is the name of your first pet?','Dog');
INSERT INTO "User" ("Username", "FirstName", "SurName", "Password", "Admin", "Mood", "SecurityQuestion", "SecurityAnswer") VALUES ('Guest30','Guest','30',NULL,'N',2,NULL,NULL);
