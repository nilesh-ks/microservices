package com.project.accounts.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;

@Schema(
        name = "Response",
        description = "Schema to hold successful response information"
)
@Data @AllArgsConstructor
public class ResponseDto {

    @Schema(
            description = "Status code in the response", examples = "200, 201, 400, 500"
    )
    private String statusCode;

    @Schema(
            description = "Status message in the response", examples = "OK, Created, Bad Request, Internal Server Error"
    )
    private String statusMessage;
}
