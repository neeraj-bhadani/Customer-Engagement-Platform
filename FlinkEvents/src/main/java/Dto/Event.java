package Dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class Event {
    private String event_id;
    private String event_category;
    private String insert_id;
    private String timestamp;
    private String user_id;
    private String source_id;
    private String device_id;
    private String event_date;

    // Additional fields
    private String product_id;
    private String product_name;
    private Integer quantity;
    private Double price;
    private String search_query;
    private String payment_method;
    private Double amount;
    private String login_method;
    private String app_version;
    private String order_id;
    private Double order_total;
}
