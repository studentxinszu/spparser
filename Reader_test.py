from spparser import Reader,Writer, AsyncReader, AsyncWriter
import asyncio
from idataapi_transform import ProcessFactory, GetterConfig, WriterConfig
import time

async def main():
    getter = AsyncReader.async_mongo_reader(query={"id":{"$exists":True}},collection="xiaohongshu_post_id_update_to_20200719", host="120.79.97.220",port=55555, database="jinmin_data",username="jinmin", password="jinmin", batch_size=5,max_read_lines=1000)
    with AsyncWriter.async_mongo_writer(collection="test1", host="120.79.97.220",port=55555, database="jinmin_data",username="jinmin", password="jinmin") as writer:
        async for items in getter:
            for item in items:
                print(item)
            await writer.write(items)
            #for item in items:
                # Parser process

async def idata():
    rconfig =  GetterConfig.RMongoConfig("xiaohongshu_post_id_update_to_20200719",host='120.79.97.220',port='55555',username='jinmin',password='jinmin',database='jinmin_data',per_limit=100,max_limit=1000,max_retry=10)
    getter = ProcessFactory.create_getter(rconfig)
    wconfig = Writer.WMongoConfig("test2",host='120.79.97.220',port='55555',username='jinmin',password='jinmin',database='jinmin_data',per_limit=100,max_limit=1000,max_retry=10)
    with ProcessFactory.create_writer(wconfig) as writer:
        async for items in getter:
            await writer.write(items)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    ts1 = time.time()
    loop.run_until_complete(main())
    t1 = time.time() - ts1

    ts2 = time.time()
    loop.run_until_complete(idata())
    t2 = time.time() - ts2

    print(t1, t2)
