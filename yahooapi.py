import yahooapi.jlp as jlp

client = jlp.JIMServiceAPI("your_apikey")
result = client.conversion(sentence=u"かなかんじへんかんたいしょうのてきすとです")
for i in result.Result.SegmentList.Segment[0].CandidateList.Candidate:
  print(i)
