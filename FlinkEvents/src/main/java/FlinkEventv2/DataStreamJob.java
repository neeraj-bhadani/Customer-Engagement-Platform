package FlinkEventv2;

import Deserializer.JSONValueDeserializationSchema;
import Dto.Event;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.connector.elasticsearch.sink.Elasticsearch7SinkBuilder;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.elasticsearch7.shaded.org.apache.http.HttpHost;
import org.apache.flink.elasticsearch7.shaded.org.elasticsearch.action.index.IndexRequest;
import org.apache.flink.elasticsearch7.shaded.org.elasticsearch.client.Requests;
import org.apache.flink.elasticsearch7.shaded.org.elasticsearch.common.xcontent.XContentType;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

import static utils.JsonUtil.convertEventToJson;


public class DataStreamJob {

	public static void main(String[] args) throws Exception {
		// Sets up the execution environment, which is the main entry point
		// to building Flink applications.
		final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

		String topic = "events";

		KafkaSource<Event> source = KafkaSource.<Event>builder()
				.setBootstrapServers("localhost:9092")
						.setTopics(topic)
								.setGroupId("flink-group")
										.setStartingOffsets(OffsetsInitializer.earliest())
												.setValueOnlyDeserializer(new JSONValueDeserializationSchema())
														.build();


		DataStream<Event> eventStream = env.fromSource(source, WatermarkStrategy.noWatermarks(), "Kafka source");
		eventStream.print();

		eventStream.sinkTo(
				new Elasticsearch7SinkBuilder<Event>()
						.setBulkFlushMaxActions(1)
						.setHosts(new HttpHost("localhost", 9200, "http"))
						.setEmitter((event, runtimeContext, requestIndexer) -> {
							String json = convertEventToJson(event);
							IndexRequest indexRequest = Requests.indexRequest()
									.index("events")
									.id(event.getInsert_id())
									.source(json, XContentType.JSON);
							requestIndexer.add(indexRequest);
						})
//						.setBulkFlushMaxActions(1) // Flush after every single action
//						.setBulkFlushInterval(1000) // Flush every second
						.build()
		).name("Elasticsearch Sink");
		// Execute program, beginning computation.
		env.execute("Flink Java API Skeleton");
	}
}
