-- upgrade --
ALTER TABLE "lesson" DROP CONSTRAINT "lesson_title_key";
-- downgrade --
ALTER TABLE "lesson" ADD CONSTRAINT "lesson_title_key" UNIQUE ("title");