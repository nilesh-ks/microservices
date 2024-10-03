package com.project.accounts.dto;

import com.project.accounts.entity.Accounts;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.Data;

@Data
public class CustomerDto {

    @NotEmpty(message = "Name cannot be null or empty")
    @Size(min = 5, max = 50, message = "Name must be between 5 and 50 characters")
    private String name;

    @NotEmpty(message = "Email address cannot be null or empty")
    @Email(message = "Invalid email address")
    private String email;

    @Pattern(regexp = "^[0-9]{10}$", message = "Mobile number should consist of 10 digits")
    private String mobileNumber;

    private AccountsDto accountsDto;
}
