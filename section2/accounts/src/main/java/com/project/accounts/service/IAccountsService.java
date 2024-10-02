package com.project.accounts.service;

import com.project.accounts.dto.CustomerDto;

public interface IAccountsService {

    /**
     * Creates a new account based on the provided customer details.
     *
     * @param customerDto	The customer details to be used for account creation.
     */
    void createAccount(CustomerDto customerDto);

    CustomerDto fetchAccount(String mobileNumber);

    boolean updateAccount(CustomerDto customerDto);
}
