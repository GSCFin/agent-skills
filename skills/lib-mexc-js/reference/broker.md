# Broker

Source: https://www.mexc.com/api-docs/broker/mexc-broker-introduction

On this page

# MEXC Broker Introduction

MEXC is committed to building crypto infrastructure, with API broker partners that provide valuable services being an essential part of the MEXC ecosystem. To reward the partners, MEXC now provides privileges for MEXC brokers, including trading rebates and marketing support.

To apply for a partnership, please contact: [broker@mexc.com](mailto:broker@mexc.com "broker@mexc.com")

## Broker Modes Supported by MEXC

### 1\. API Broker

This includes copy trade platforms, trading bots, quantitative strategy platforms, or other asset management platforms with more than 500 people, etc. Users can authorize the API key to the API broker, and the API broker will send the trading orders containing the broker ID on behalf of the user and receive profit shares from fees.

### 2\. Independent Broker

This includes wallet platforms, market data platforms, aggregation trading platforms, stockbrokers, as well as stock and securities trading platforms, etc., all of which have their own independent users. MEXC can provide order matching systems, account management systems, settlement systems, as well as main and sub-account systems, etc. Independent brokers can share the trading fluidity and depth over the MEXC platform and receive profit shares from fees.

### 3\. Oauth Broker

**Introduction**

The third-party application connected to MEXC OAuth 2.0 can provide MEXC users the one-click trade function. The details are as follows:  
MEXC users only need to perform authorization in the third-party application in one click, and they can start trading without directly providing the API key to the third-party application.  
MEXC OAuth 2.0 is supported on Web version, and is developed based on the OAuth 2.0 protocol (RFC 6749).

## Broker Services Provided by MEXC

### 1\. API Brokers

The user signs up at MEXC, applies for API Key in MEXC, and provides it to the broker.

*   Supports trading pairs set by users
*   Supports API Key renewal, and avoids multiple binding.

![](/api-docs-assets/img/broker/brokeren1.png)

### 2\. Independent Brokers

Brokers have their own brands and separate account systems.Brokers create separate sub-accounts for users to trade under the Master account. Sub-accounts support deposit and withdrawal.

*   Support sub-account deposit and withdrawal
*   Support sub-account transfer

![](/api-docs-assets/img/broker/brokeren2.png)

### 3\. Integration Procedure

1.  Sign up for an account on the official website and apply to become a broker. You must first apply to become a MEXC broker using [MEXC Broker Project Application Form](https://docs.google.com/forms/d/e/1FAIpQLSed5ocsfcvUU0xtq0dgJ2KIGBwzjQf3tKfhwi7phuRvxdKjsg/viewform "MEXC Broker Project Application Form").
2.  Once approved, a dedicated account manager will provide you the corresponding developer docs.
3.  OAuth Rebate Settings  
    After integration of the OAuth broker, when placing an order, you need to fill in the exclusive broker\_id in the source field of the header to be used as an identifier for the rebate order statistics.

**Authorization Mode Introduction**

The authorization mode provided by MEXC OAuth 2.0: Authorization code mode.

Authorization Mode

Description

Scenario

Authorization Mode

User authorizes a third-party application to provide client\_secret and obtain the authorization code, which is then used to obtain access token and refresh token.

The application has a server, which can store the application key and interact the key with the MEXCOAuth server.

![](/api-docs-assets/img/broker/brokeren3.png)

**Authorization Code Mode**

After the user jumps to the MEXC authorization page through the third-party application and authorizes it, the third-party application can exchange the authorization code for an access token, and access the data resources authorized by the user by using MEXC OpenAPI.