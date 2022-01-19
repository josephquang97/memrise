import pytest
import io
# import tempfile
import sqlite3

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

-- INSERT

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

-- INSERT SENTENSE
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('she studied ALL night for her CHEMISTRY final.', 'cô ấy đã học SUỐT đêm để chuẩn bị cho bài thi HÓA cuối kỳ.', 'ʃi ˈstʌdid ɔl naɪt fɔr hɜr ˈkɛməstri ˈfaɪnəl.', 'true', 'true', '1');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('we WORKED for HOURS on our MATH assignment.', 'chúng tôi đã LÀM VIỆC suốt NHIỀU GIỜ chuẩn bị cho bài tập TOÁN.', 'wi wɜrkt fɔr ˈaʊərz ɑn ˈaʊər mæθ əˈsaɪnmənt.', 'true', 'true', '1');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('he FORGOT to HAND in his ESSAY.', 'anh ấy ĐÃ QUÊN đem theo BÀI LUẬN.', 'hi fərˈgɑt tu hænd ɪn hɪz ˈɛˌseɪ.', 'true', 'true', '1');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('she POINTED out a SILLY mistake I had MADE.', 'cô ấy ĐÃ CHỈ ra sai lầm NGỚ NGẨN mà tôi đã PHẠM.', 'ʃi ˈpɔɪntəd aʊt ə ˈsɪli mɪsˈteɪk aɪ hæd meɪd.', 'true', 'true', '1');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('that''s your END OF YEAR project.', 'đó là dự án cuối năm của bạn.', 'ðæts jʊər ɛnd ʌv jɪr ˈprɑʤɛkt.', 'true', 'true', '1');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('we HAD to have LUNCH on the GO today.', 'chúng tôi đã phải ăn trưa vào chuyến đi ngày hôm nay.', 'wi hæd tu hæv lʌnʧ ɑn ðə goʊ təˈdeɪ.', 'true', 'true', '2');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('he ATE a VEGETARIAN burger', 'anh ăn một chiếc burger chay', 'hi eɪt ə ˌvɛʤəˈtɛriən ˈbɜrgər', 'true', 'true', '2');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('she ALWAYS eats a GARDEN salad for LUNCH.', 'cô ấy luôn ăn một món salad vườn cho bữa trưa.', 'ʃi ˈɔlˌweɪz its ə ˈgɑrdən ˈsæləd fɔr lʌnʧ.', 'true', 'true', '2');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('they NEVER eat LUNCH during the WEEK.', 'họ không bao giờ ăn trưa trong tuần.', 'ðeɪ ˈnɛvər it lʌnʧ ˈdʊrɪŋ ðə wik.', 'true', 'true', '2');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('her BUSINESS lunch was CANCELLED.', 'bữa trưa kinh doanh của cô đã bị hủy bỏ.', 'hɜr ˈbɪznəs lʌnʧ wʌz ˈkænsəld.', 'true', 'true', '2');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('you NEED to be READY by FIVE o''clock.', 'bạn cần sẵn sàng vào năm giờ.', 'ju nid tu bi ˈrɛdi baɪ faɪv əˈklɑk.', 'true', 'true', '3');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('we should ALWAYS be PREPARED for a SITUATION like this.', 'chúng ta nên luôn luôn chuẩn bị cho một tình huống như thế này.', 'wi ʃʊd ˈɔlˌweɪz bi priˈpɛrd fɔr ə ˌsɪʧuˈeɪʃən laɪk ðɪs.', 'true', 'true', '3');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I REALLY need to GO now.', 'tôi thực sự cần phải đi ngay bây giờ.', 'aɪ ˈrɪli nid tu goʊ naʊ.', 'true', 'true', '3');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I''ve READ this BOOK a THOUSAND times.', 'tôi đã đọc cuốn sách này một ngàn lần.', 'aɪv rid ðɪs bʊk ə ˈθaʊzənd taɪmz.', 'true', 'true', '3');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('you MUST wear a MASK at ALL times inside the SCHOOL.', 'bạn phải đeo mặt nạ mọi lúc trong trường.', 'ju mʌst wɛr ə mæsk æt ɔl taɪmz ɪnˈsaɪd ðə skul.', 'true', 'true', '3');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('DON''T doubt yourself.', 'đừng nghi ngờ chính mình.', 'doʊnt daʊt jərˈsɛlf.', 'true', 'true', '4');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('if you don''t ASK, you won''t GET.', 'nếu bạn không hỏi, bạn sẽ không nhận được.', 'ɪf ju doʊnt æsk, ju woʊnt gɛt.', 'true', 'true', '4');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('you know MORE than you THINK you do.', 'bạn biết nhiều hơn bạn nghĩ bạn làm.', 'ju noʊ mɔr ðæn ju θɪŋk ju du.', 'true', 'true', '4');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('ACCEPT who you ARE.', 'chấp nhận bạn là ai.', 'ækˈsɛpt hu ju ɑr.', 'true', 'true', '4');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('it''s not the MOUNTAIN we conquer, but OURSELVES.', 'đó không phải là ngọn núi chúng tôi chinh phục, mà là chính chúng ta.', 'ɪts nɑt ðə ˈmaʊntən wi ˈkɑŋkər, bʌt aʊərˈsɛlvz.', 'true', 'true', '4');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('when you have CONFIDENCE, you can do ANYTHING.', 'khi bạn có sự tự tin, bạn có thể làm bất cứ điều gì.', 'wɛn ju hæv ˈkɑnfədəns, ju kæn du ˈɛniˌθɪŋ.', 'true', 'true', '4');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('the most BEAUTIFUL thing you can WEAR is CONFIDENCE.', 'điều đẹp nhất bạn có thể mặc là sự tự tin.', 'ðə moʊst ˈbjutəfəl θɪŋ ju kæn wɛr ɪz ˈkɑnfədəns.', 'true', 'true', '4');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('check it OUT if you WANT to.', 'kiểm tra xem nếu bạn muốn.', 'ʧɛk ɪt aʊt ɪf ju wɑnt tu.', 'true', 'true', '5');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I''d LOVE to GO there someday.', 'tôi muốn đến đó một ngày nào đó.', 'aɪd lʌv tu goʊ ðɛr ˈsʌmˌdeɪ.', 'true', 'true', '5');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I''ll CALL you after LUNCH.', 'tôi sẽ gọi cho bạn sau bữa trưa.', 'aɪl kɔl ju ˈæftər lʌnʧ.', 'true', 'true', '5');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I''m NOT in the MOOD for that.', 'tôi không có tâm trạng cho điều đó.', 'aɪm nɑt ɪn ðə mud fɔr ðæt.', 'true', 'true', '5');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I need a BREAK before the NEXT one.', 'tôi cần nghỉ ngơi trước lần tiếp theo.', 'aɪ nid ə breɪk bɪˈfɔr ðə nɛkst wʌn.', 'true', 'true', '5');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I WENT to the STORE.', 'tôi đã tới cửa hàng.', 'aɪ wɛnt tu ðə stɔr.', 'true', 'true', '6');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I''m GLAD you LIKE it.', 'tôi vui vì bạn thích nó.', 'aɪm glæd ju laɪk ɪt.', 'true', 'true', '6');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('take a LEFT at the LIGHT.', 'tới cây CỘT ĐÈN thì RẼ TRÁI.', 'teɪk ə lɛft æt ðə laɪt.', 'true', 'true', '6');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I have a LOT to DO.', 'tôi có rất nhiều việc phải làm.', 'aɪ hæv ə lɑt tu du.', 'true', 'true', '6');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I''ll GIVE it a SHOT.', 'tao sẽ THỬ làm điều đó.', 'aɪl gɪv ɪt ə ʃɑt.', 'true', 'true', '6');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I''m HAPPY to HEAR that!', 'Tôi MỪNG vì điều đó.', 'aɪm ˈhæpi tu hir ðæt!', 'true', 'true', '7');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('It DEPENDS what they SAY.', 'Chuyện đó còn PHỤ THUỘC vào họ nói gì nữa.', 'ɪt dɪˈpɛndz wʌt ðeɪ seɪ.', 'true', 'true', '7');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I''ll HAVE to TRY that.', 'Tao NHẤT ĐỊNH phải THỬ nó.', 'aɪl hæv tu traɪ ðæt.', 'true', 'true', '7');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('We should REALLY get GOING.', 'Chúng ta thực sự nên đi thôi.', 'wi ʃʊd ˈrɪli gɛt ˈgoʊɪŋ.', 'true', 'true', '7');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('It''s was a BIG SUCCESS.', 'Đó là một thành công lớn.', 'ɪts wʌz ə bɪg səkˈsɛs.', 'true', 'true', '7');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I''ll TRY it on FRIDAY.', 'Thứ Sáu này tôi sẽ thử.', 'aɪl traɪ ɪt ɑn ˈfraɪdi.', 'true', 'true', '8');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I ACTUALLY have to GO.', 'Thực ra tôi phải đi rồi.', 'aɪ ˈækʧuəli hæv tu goʊ.', 'true', 'true', '8');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I''m SURE they''ll be FINE.', 'CHẮC họ sẽ ỔN thôi.', 'aɪm ʃʊr ðeɪl bi faɪn.', 'true', 'true', '8');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('We''ll DECIDE about that LATER.', 'Chuyện đó tính sau đi.', 'wil ˌdɪˈsaɪd əˈbaʊt ðæt ˈleɪtər.', 'true', 'true', '8');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I APPRECIATE what you DID.', 'Tôi TRÂN TRỌNG những gì bạn ĐÃ LÀM.', 'aɪ əˈpriʃiˌeɪt wʌt ju dɪd.', 'true', 'true', '8');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('Let''s SEE how it GOES.', 'Cùng xem nó diễn ra thế nào nhé.', 'lɛts si haʊ ɪt goʊz.', 'false', 'false', '9');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I DOUBT that will WORK.', 'Tao LO là nó KHÔNG hoạt động.', 'aɪ daʊt ðæt wɪl wɜrk.', 'false', 'false', '9');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I''d LOVE to HEAR from you.', 'Rất mong nhận được phản hồi từ bạn.', 'aɪd lʌv tu hir frʌm ju.', 'false', 'false', '9');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('it''s NOT that FAR from here.', 'Cũng KHÔNG XA lắm.', 'ɪts nɑt ðæt fɑr frʌm hir.', 'false', 'false', '9');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I LEARNED a LOT there.', 'Tôi ĐÃ HỌC được khá NHIỀU ở đó.', 'aɪ lɜrnd ə lɑt ðɛr.', 'false', 'false', '9');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I''ll SEE you after WORK.', 'Gặp sau giờ làm nhe.', 'aɪl si ju ˈæftər wɜrk.', 'false', 'false', '10');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('we should STAY until the END.', 'chúng ta nên Ở LẠI đến HẾT buổi.', 'wi ʃʊd steɪ ənˈtɪl ði ɛnd.', 'false', 'false', '10');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('you can TAKE one if you WANT.', 'Mày có thể lấy MỘT cái nếu MUỐN.', 'ju kæn teɪk wʌn ɪf ju wɑnt.', 'false', 'false', '10');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('it will be at LEAST a WEEK.', 'ÍT NHẤT cũng phải MỘT TUẦN.', 'ɪt wɪl bi æt list ə wik.', 'false', 'false', '10');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I''ll CHECK if we can DO it.', 'tôi sẽ KIỂM TRA xem chúng ta có thể LÀM được không.', 'aɪl ʧɛk ɪf wi kæn du ɪt.', 'false', 'false', '10');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I WONDER why they DID that.', 'tao TỰ HỎI không biết tại sao họ LÀM như vậy.', 'aɪ ˈwʌndər waɪ ðeɪ dɪd ðæt.', 'false', 'false', '11');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I BORROWED it from a FRIEND.', 'tao MƯỢN nó từ một người bạn.', 'aɪ ˈbɑˌroʊd ɪt frʌm ə frɛnd.', 'false', 'false', '11');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('You HAVE to be PATIENT.', 'mày PHẢI kiên NHẪN.', 'ju hæv tu bi ˈpeɪʃənt.', 'false', 'false', '11');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('that was a BIG DECISION.', 'đó là một QUYẾT ĐỊNH QUAN TRỌNG.', 'ðæt wʌz ə bɪg dɪˈsɪʒən.', 'false', 'false', '11');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('That''s one of my FAVORITE BOOKS.', 'Đó là một trong những CUỐN SÁCH YÊU THÍCH NHẤT của tao.', 'ðæts wʌn ʌv maɪ ˈfeɪvərɪt bʊks.', 'false', 'false', '11');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I''ll SEE you on MONDAY!', 'Hẹn gặp lại vào THỨ HAI nha!', 'aɪl si ju ɑn ˈmʌndi!', 'false', 'false', '12');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I''m CURIOUS what you THINK.', 'Tao hơi THẮC MẮC là mày đang nghĩ gì.', 'aɪm ˈkjʊriəs wʌt ju θɪŋk.', 'false', 'false', '12');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('we MET in ELEMENTARY school.', 'bọn tao gặp nhau hồi tiểu học.', 'wi mɛt ɪn ˌɛləˈmɛntri skul.', 'false', 'false', '12');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I''m FEELING GOOD about that.', 'Tao thấy chuyện đó cũng tốt mà.', 'aɪm ˈfilɪŋ gʊd əˈbaʊt ðæt.', 'false', 'false', '12');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('TRY not to OVERTHINK it.', 'ĐỪNG SUY NGHĨA quá nhiều!', 'traɪ nɑt tu ˌoʊvərˈθɪŋk ɪt.', 'false', 'false', '12');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I DID it this MORNING.', 'Tao mới làm hồi sáng này.', 'aɪ dɪd ɪt ðɪs ˈmɔrnɪŋ.', 'false', 'false', '13');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('they SHOULDN''T have DONE that.', 'Lẽ ra bọn họ KHÔNG NÊN làm vậy.', 'ðeɪ ˈʃʊdənt hæv dʌn ðæt.', 'false', 'false', '13');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('Just LEAVE it on the COUNTER.', 'Cứ để nó ở máy đếm đi.', 'ʤʌst liv ɪt ɑn ðə ˈkaʊntər.', 'false', 'false', '13');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I''m WORRIED about my FRIEND.', 'tôi thấy LO LẮNG về một đứa bạn.', 'aɪm ˈwɜrid əˈbaʊt maɪ frɛnd.', 'false', 'false', '13');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('It SOUNDS like it would be PERFECT.', 'Nghe có vẻ nó sẽ rất TUYỆT VỜI.', 'ɪt saʊndz laɪk ɪt wʊd bi ˈpɜrˌfɪkt.', 'false', 'false', '13');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I WONDER what HAPPENED with that.', 'tao TỰ HỎI điều gì ĐÃ XẢY RA với nó.', 'aɪ ˈwʌndər wʌt ˈhæpənd wɪð ðæt.', 'false', 'false', '14');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('He ORDERED it on MONDAY.', 'Anh ấy ĐÃ ĐẶT nó vào THỨ HAI.', 'hi ˈɔrdərd ɪt ɑn ˈmʌndi.', 'false', 'false', '14');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('It COULDN''T have been BETTER.', 'KHÔNG THỂ tốt HƠN được nữa.', 'ɪt ˈkʊdənt hæv bɪn ˈbɛtər.', 'false', 'false', '14');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('SORRY to BOTHER you again.', 'XIN LỖI đã LÀM PHIỀN bạn lần nữa.', 'ˈsɑri tu ˈbɑðər ju əˈgɛn.', 'false', 'false', '14');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('We''ve been WAITING for an HOUR.', 'Chúng tôi đã ĐỢI cả TIẾNG rồi.', 'wiv bɪn ˈweɪtɪŋ fɔr ən ˈaʊər.', 'false', 'false', '14');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('that sounds GOOD, but I''m NOT SURE.', 'Nghe có vẻ HAY, nhưng tao cũng KHÔNG CHẮC CHẮN.', 'ðæt saʊndz gʊd, bʌt aɪm nɑt ʃʊr.', 'false', 'false', '15');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('they''ll TELL us by the END of the WEEK.', 'Họ sẽ trả lời chúng tôi vào CUỐI tuần này.', 'ðeɪl tɛl ʌs baɪ ði ɛnd ʌv ðə wik.', 'false', 'false', '15');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('It LOOKS like it MIGHT RAIN.', 'Có vẻ trời SẮP MƯA.', 'ɪt lʊks laɪk ɪt maɪt reɪn.', 'false', 'false', '15');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I''ve KNOWN her for a LONG TIME.', 'tôi BIẾT cô ấy LÂU LẮM rồi.', 'aɪv noʊn hɜr fɔr ə lɔŋ taɪm.', 'false', 'false', '15');
INSERT INTO "sentense" ("sentense", "meaning", "ipa", "audio1", "audio2", "topic_id") VALUES ('I CAN''T TELL if I''m SICK.', 'Tôi KHÔNG CHẮC liệu rằng tôi có BỆNH KHÔNG.', 'aɪ kænt tɛl ɪf aɪm sɪk.', 'false', 'false', '15');

"""


@pytest.fixture
def cursor(filename):
    conn = sqlite3.Connection(filename)
    cur = conn.cursor()
    yield cur


@pytest.fixture
def mock_stdin(content,monkeypatch):
	monkeypatch.setattr('sys.stdin',io.StringIO(content))