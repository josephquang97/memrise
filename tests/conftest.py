import sqlite3
import pytest

from PyMemAPI.PyMemAPI import Memrise
@pytest.fixture(scope="session")  
def cmd():
	COMMAND = """
DROP TABLE IF EXISTS "sentense" ;
DROP TABLE IF EXISTS "topic"  ;

CREATE TABLE "topic" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"status"	TEXT DEFAULT 'local' CHECK("status" IN ('stream', 'local')),
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "sentense" (
	"id"	INTEGER NOT NULL UNIQUE,
	"sentense"	TEXT NOT NULL,
	"meaning"	TEXT,
	"ipa"	INTEGER,
	"audio1"	TEXT DEFAULT 'false' CHECK("audio1" IN ('true', 'false')),
	"audio2"	TEXT DEFAULT 'false' CHECK("audio2" IN ('true', 'false')),
	"topic_id"	INTEGER NOT NULL,
	FOREIGN KEY("topic_id") REFERENCES "topic"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);


-- INSERT TOPICs
INSERT INTO "topic" ("id", "name", "status") VALUES ('1', 'School Work', 'local');
INSERT INTO "topic" ("id", "name", "status") VALUES ('2', 'Lunch on the go', 'local');
INSERT INTO "topic" ("id", "name", "status") VALUES ('3', 'Speaking about time', 'local');
INSERT INTO "topic" ("id", "name", "status") VALUES ('4', 'Famous quotes on self-confidence', 'local');
INSERT INTO "topic" ("id", "name", "status") VALUES ('5', 'I''d love to go!', 'local');
INSERT INTO "topic" ("id", "name", "status") VALUES ('6', 'Glad you like it!', 'local');
INSERT INTO "topic" ("id", "name", "status") VALUES ('7', 'A big success', 'local');
INSERT INTO "topic" ("id", "name", "status") VALUES ('8', 'I Appriaciate it!', 'local');
INSERT INTO "topic" ("id", "name", "status") VALUES ('9', 'I learned a lot', 'local');
INSERT INTO "topic" ("id", "name", "status") VALUES ('10', 'We should stay', 'local');
INSERT INTO "topic" ("id", "name", "status") VALUES ('11', 'I wonder why', 'local');
INSERT INTO "topic" ("id", "name", "status") VALUES ('12', 'See you on Monday!', 'local');
INSERT INTO "topic" ("id", "name", "status") VALUES ('13', 'It sounds perfect!', 'local');
INSERT INTO "topic" ("id", "name", "status") VALUES ('14', 'Sorry to bother you!', 'local');
INSERT INTO "topic" ("id", "name", "status") VALUES ('15', 'I can''t say for sure', 'local');

-- INSERT sentense
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('she studied ALL night for her CHEMISTRY final.', '1');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('we WORKED for HOURS on our MATH assignment.', '1');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('he FORGOT to HAND in his ESSAY.', '1');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('she POINTED out a SILLY mistake I had MADE.', '1');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('that''s your END OF YEAR project.', '1');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('we HAD to have LUNCH on the GO today.', '2');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('he ATE a VEGETARIAN burger', '2');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('she ALWAYS eats a GARDEN salad for LUNCH.', '2');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('they NEVER eat LUNCH during the WEEK.', '2');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('her BUSINESS lunch was CANCELLED.', '2');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('you NEED to be READY by FIVE o''clock.', '3');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('we should ALWAYS be PREPARED for a SITUATION like this.', '3');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I REALLY need to GO now.', '3');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I''ve READ this BOOK a THOUSAND times.', '3');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('you MUST wear a MASK at ALL times inside the SCHOOL.', '3');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('DON''T doubt yourself.', '4');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('if you don''t ASK, you won''t GET.', '4');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('you know MORE than you THINK you do.', '4');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('ACCEPT who you ARE.', '4');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('it''s not the MOUNTAIN we conquer, but OURSELVES.', '4');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('when you have CONFIDENCE, you can do ANYTHING.', '4');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('the most BEAUTIFUL thing you can WEAR is CONFIDENCE.', '4');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('check it OUT if you WANT to.', '5');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I''d LOVE to GO there someday.', '5');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I''ll CALL you after LUNCH.', '5');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I''m NOT in the MOOD for that.', '5');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I need a BREAK before the NEXT one.', '5');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I WENT to the STORE.', '6');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I''m GLAD you LIKE it.', '6');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('take a LEFT at the LIGHT.', '6');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I have a LOT to DO.', '6');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I''ll GIVE it a SHOT.', '6');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I''m HAPPY to HEAR that!', '7');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('It DEPENDS what they SAY.', '7');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I''ll HAVE to TRY that.', '7');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('We should REALLY get GOING.', '7');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('It''s was a BIG SUCCESS.', '7');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I''ll TRY it on FRIDAY.', '8');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I ACTUALLY have to GO.', '8');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I''m SURE they''ll be FINE.', '8');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('We''ll DECIDE about that LATER.', '8');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I APPRECIATE what you DID.', '8');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('Let''s SEE how it GOES.', '9');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I DOUBT that will WORK.', '9');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I''d LOVE to HEAR from you.', '9');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('it''s NOT that FAR from here.', '9');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I LEARNED a LOT there.', '9');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I''ll SEE you after WORK.', '10');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('we should STAY until the END.', '10');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('you can TAKE one if you WANT.', '10');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('it will be at LEAST a WEEK.', '10');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I''ll CHECK if we can DO it.', '10');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I WONDER why they DID that.', '11');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I BORROWED it from a FRIEND.', '11');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('You HAVE to be PATIENT.', '11');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('that was a BIG DECISION.', '11');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('That''s one of my FAVORITE BOOKS.', '11');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I''ll SEE you on MONDAY!', '12');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I''m CURIOUS what you THINK.', '12');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('we MET in ELEMENTARY school.', '12');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I''m FEELING GOOD about that.', '12');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('TRY not to OVERTHINK it.', '12');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I DID it this MORNING.', '13');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('they SHOULDN''T have DONE that.', '13');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('Just LEAVE it on the COUNTER.', '13');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I''m WORRIED about my FRIEND.', '13');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('It SOUNDS like it would be PERFECT.', '13');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I WONDER what HAPPENED with that.', '14');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('He ORDERED it on MONDAY.', '14');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('It COULDN''T have been BETTER.', '14');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('SORRY to BOTHER you again.', '14');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('We''ve been WAITING for an HOUR.', '14');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('that sounds GOOD, but I''m NOT SURE.', '15');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('they''ll TELL us by the END of the WEEK.', '15');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('It LOOKS like it MIGHT RAIN.', '15');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I''ve KNOWN her for a LONG TIME.', '15');
INSERT INTO "sentense" ("sentense", "topic_id") VALUES ('I CAN''T TELL if I''m SICK.', '15');
""" 
	yield COMMAND


#Conf for testing database connection
@pytest.fixture(scope="session")  
def db_conn():
    with sqlite3.Connection("./course/course.db") as conn:
    	yield conn


@pytest.fixture(scope="session")
def course(monkeypatch):
	client = Memrise()
	user = {"Enter username: ":"dummy_user", "Enter password: ":"testing2022", "Make your choice: ": "1"}
	monkeypatch.setattr("builtins.input", lambda msg: user[msg])
	client.login()
	crse =  client.select_course()
	yield crse