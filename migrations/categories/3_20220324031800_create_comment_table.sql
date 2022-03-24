-- upgrade --
CREATE TABLE IF NOT EXISTS "comment" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "content" TEXT NOT NULL,
    "writed_at" TIMESTAMPTZ,
    "likes" INT NOT NULL,
    "external_id" VARCHAR(50) NOT NULL,
    "author_id" INT REFERENCES "user_profile" ("id") ON DELETE CASCADE,
    "lesson_id" INT REFERENCES "lesson" ("id") ON DELETE CASCADE
);
-- downgrade --
DROP TABLE IF EXISTS "comment";