from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        -- This migration converts the existing JSONB structure to individual columns
        -- If you have existing data in the JSONB format, you'll need to migrate it manually
        
        -- First, backup your existing data:
        -- CREATE TABLE blog_backup AS SELECT * FROM blog;
        
        -- Add new columns
        ALTER TABLE "blog" ADD "title" VARCHAR(255);
        ALTER TABLE "blog" ADD "text" TEXT NOT NULL DEFAULT '';
        ALTER TABLE "blog" ADD "tags" JSONB DEFAULT '[]';
        
        -- If you have existing data in the 'data' column, uncomment and run:
        -- UPDATE blog SET 
        --     title = data->>'title',
        --     text = data->>'text',
        --     tags = data->'tags'
        -- WHERE data IS NOT NULL;
        
        -- Drop the old data column after migration:
        -- ALTER TABLE "blog" DROP COLUMN "data";
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        -- Restore the original JSONB structure
        ALTER TABLE "blog" ADD "data" JSONB;
        
        -- Migrate data back to JSONB format:
        UPDATE blog SET data = jsonb_build_object(
            'title', title,
            'text', text,
            'tags', tags
        );
        
        -- Drop the individual columns
        ALTER TABLE "blog" DROP COLUMN "title";
        ALTER TABLE "blog" DROP COLUMN "text"; 
        ALTER TABLE "blog" DROP COLUMN "tags";
    """