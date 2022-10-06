-- upgrade --
ALTER TABLE "lesson" ALTER COLUMN "title" TYPE VARCHAR(200) USING "title"::VARCHAR(200);
-- downgrade --
ALTER TABLE "lesson" ALTER COLUMN "title" TYPE VARCHAR(100) USING "title"::VARCHAR(100);
