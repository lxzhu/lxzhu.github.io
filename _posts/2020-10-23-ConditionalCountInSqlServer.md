---
title: Conditional Count() in Sql Server
tags: [count, sql, sql server]
author: liangxiong zhu(lxzhu@outlook.com)
---

Usually, when you want to count on selected rows, you put a where clause. But, how about if you have multiple count() 
in select subclause but with different conditions?

I have a table named TypedServiceRequests in database. Among other business fields, it contains following fields

|column | data type | description |
|---|---|---|
|Id|bigint|primary key|
|BatchId|bigint not null| The id of the batch of this request|
|BatchItemType|nvarchar(100) not null| the type of data this request is sending|
|AckDateTime|datetime null| The moment when target service replies. It is null if no reply has been received.|

Now, I want to have a query which returns 

1. The total number of requests of a specified batch
1. The total number of acked requests of the specified batch
1. The total number of person requests of the specified batch
1. The total number of acked person requets of the specified batch

**Based on a logic that, null does not count in count function, I have following TSQL.**

```sql

declare @batchId bigint;
set @batchId=11497;

select 
count(1) as Total,
count(AckDateTime) as Acked,
count(case 
		when BatchItemType='Person' then 1 
		else null 
	 end) as PersonTotal,
count(case 
		when BatchItemType='Person' and AckDateTime is not null then 1 
		else null 
	end) as PersonAcked
from TypedServiceRequests 
where BatchId=@batchId

```

