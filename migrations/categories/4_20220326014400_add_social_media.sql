-- upgrade --
CREATE TABLE IF NOT EXISTS "social_media" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE,
    "base_url" VARCHAR(100) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "social_media_profile" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(100) NOT NULL,
    "external_id" VARCHAR(100) NOT NULL,
    "user_id" INT REFERENCES "user_profile" ("id") ON DELETE CASCADE,
    "social_media_id" INT REFERENCES "social_media" ("id") ON DELETE CASCADE
);
ALTER TABLE "user_profile" 
    ALTER COLUMN "name" VARCHAR(200),
    ADD COLUMN "public_profile" BOOLEAN NOT NULL DEFAULT false,
    ADD COLUMN "rank" INT NOT NULL DEFAULT 0,
    ADD COLUMN "country_code" VARCHAR(10),
    ADD COLUMN "answer_count" INT NOT NULL DEFAULT 0,
    ADD COLUMN "question_count" INT NOT NULL DEFAULT 0;
CREATE TABLE IF NOT EXISTS "user_profile_career" (
    "user_id" INT NOT NULL REFERENCES "user_profile" ("id") ON DELETE CASCADE,
    "career_id" INT NOT NULL REFERENCES "career" ("id") ON DELETE CASCADE
);
-- downgrade --
DROP TABLE IF EXISTS "social_media";
DROP TABLE IF EXISTS "social_media_profile";
ALTER TABLE "user_profile" 
    ALTER COLUMN "name" VARCHAR(100),
    DROP COLUMN "public_profile",
    DROP COLUMN "rank",
    DROP COLUMN "country_code",
    DROP COLUMN "answer_count",
    DROP COLUMN "question_count";
DROP TABLE IF EXISTS "user_profile_career";
