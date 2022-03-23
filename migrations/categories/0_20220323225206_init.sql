-- upgrade --
CREATE TABLE IF NOT EXISTS "category" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE,
    "path" VARCHAR(150) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "career" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE,
    "path" VARCHAR(150) NOT NULL UNIQUE,
    "category_id" INT NOT NULL REFERENCES "category" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "user_profile" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(100) NOT NULL UNIQUE,
    "role" VARCHAR(50) NOT NULL,
    "name" VARCHAR(100)
);
CREATE TABLE IF NOT EXISTS "course" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(100) NOT NULL UNIQUE,
    "path" VARCHAR(150) NOT NULL UNIQUE,
    "release" TIMESTAMPTZ,
    "external_id" VARCHAR(50) NOT NULL UNIQUE,
    "type" VARCHAR(50),
    "teacher_id" INT REFERENCES "user_profile" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "lesson" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "track_number" INT NOT NULL,
    "title" VARCHAR(100) NOT NULL UNIQUE,
    "path" VARCHAR(150) NOT NULL UNIQUE,
    "duration_in_seg" INT NOT NULL,
    "external_id" VARCHAR(50) NOT NULL,
    "type" VARCHAR(50) NOT NULL,
    "course_id" INT NOT NULL REFERENCES "course" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "review" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "comment" TEXT NOT NULL,
    "stars" DECIMAL(2,1) NOT NULL,
    "user_id" INT NOT NULL REFERENCES "user_profile" ("id") ON DELETE CASCADE,
    "course_id" INT NOT NULL REFERENCES "course" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_review_course__13bc82" UNIQUE ("course_id", "user_id")
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "course_career" (
    "course_id" INT NOT NULL REFERENCES "course" ("id") ON DELETE CASCADE,
    "career_id" INT NOT NULL REFERENCES "career" ("id") ON DELETE CASCADE
);
