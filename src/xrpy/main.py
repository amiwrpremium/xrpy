from typing import Union


from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet, Wallet

from xrpl.utils import xrp_to_drops

from xrpl.models.transactions import Payment, TrustSet, TrustSetFlag, OfferCreate, OfferCancel, OfferCreateFlag
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.models.response import Response

from xrpl.transaction import safe_sign_and_autofill_transaction, send_reliable_submission


def create_wallet(client: JsonRpcClient) -> Wallet:
    """
    Create a wallet

    :param client: xrpl Client
    :type client: JsonRpcClient

    :return: XRPL Wallet
    :rtype: Wallet
    """

    _wallet = generate_faucet_wallet(client)
    return _wallet


def send_transaction(client: JsonRpcClient, from_wallet: Wallet, amount: Union[int, float],
                     destination: str) -> Response:
    """
    Send a transaction

    :param client: xrpl Client
    :type client: JsonRpcClient

    :param from_wallet: XRPL Wallet
    :type from_wallet: Wallet

    :param amount: Amount to send
    :type amount: Union[int, float]

    :param destination: Destination address
    :type destination: str

    :return: Result of transaction sending attempt
    :rtype: Response
    """

    tx_payment = Payment(
        account=from_wallet.classic_address,
        amount=xrp_to_drops(amount),
        destination=destination,
    )

    tx_payment_signed = safe_sign_and_autofill_transaction(tx_payment, from_wallet, client)
    tx_response = send_reliable_submission(tx_payment_signed, client)

    return tx_response


def set_trust_line(client: JsonRpcClient, from_wallet: Wallet, currency: str, value: str, issuer: str) -> Response:
    """
    Create a trust line

    :param client: xrpl Client
    :type client: JsonRpcClient

    :param from_wallet: XRPL Wallet
    :type from_wallet: Wallet

    :param currency: Trust line currency
    :type currency: str

    :param value: Trust line value
    :type value: str

    :param issuer: Trust line issuer
    :type issuer: str

    :return: Result of Trust line creation attempt
    :rtype: Response

    ex)
        trust_set = TrustSet(
            account='rfL6jD4a9coALoR35cM9kLGGThrohuKjai',
            limit_amount=IssuedCurrencyAmount(
                currency='VGB',
                value='100000000',
                issuer='rhcyBrowwApgNonehKBj8Po5z4gTyRknaU'
            ),
            flags=TrustSetFlag.TF_SET_NO_RIPPLE,
        )

    """
    trust_set = TrustSet(
        account=from_wallet.classic_address,
        limit_amount=IssuedCurrencyAmount(
            currency=currency.upper(),
            value=value,
            issuer=issuer,
        ),
        flags=TrustSetFlag.TF_SET_NO_RIPPLE
    )

    my_tx_payment_signed = safe_sign_and_autofill_transaction(trust_set, from_wallet, client)
    tx_response = send_reliable_submission(my_tx_payment_signed, client)

    return tx_response


def create_offer(client: JsonRpcClient, from_wallet: Wallet, taker_gets_xrp: int,
                 taker_pays_currency: str, taker_pays_value: str, taker_pays_issuer: str,
                 side: str) -> Response:
    """
    Place Order

    :param client: xrpl Client
    :type client: JsonRpcClient

    :param from_wallet: XRPL Wallet
    :type from_wallet: Wallet

    :param taker_gets_xrp: amount in xrp for taker gets
    :type taker_gets_xrp: int

    :param taker_pays_currency: Currency
    :type taker_pays_currency: str

    :param taker_pays_value: Value
    :type taker_pays_value: str

    :param taker_pays_issuer: Issuer
    :type taker_pays_issuer: str

    :param side: Offer side (buy or sell)
    :type side: str

    :return: Result of order placing attempt
    :rtype: Response

    ex)
        offer_create = OfferCreate(
            account='rfL6jD4a9coALoR35cM9kLGGThrohuKjai',
            taker_gets=xrp_to_drops(2),
            taker_pays=IssuedCurrencyAmount(
                currency='VGB',
                value='20',
                issuer='rhcyBrowwApgNonehKBj8Po5z4gTyRknaU',
            ),
            # flags=OfferCreateFlag.TF_SELL
        )
    """

    offer_create = OfferCreate(
        account=from_wallet.classic_address,
        taker_gets=xrp_to_drops(taker_gets_xrp),
        taker_pays=IssuedCurrencyAmount(
            currency=taker_pays_currency,
            value=taker_pays_value,
            issuer=taker_pays_issuer,
        ),
        flags=OfferCreateFlag.TF_SELL if side.lower() == 'sell' else None
    )

    my_tx_payment_signed = safe_sign_and_autofill_transaction(offer_create, from_wallet, client)
    tx_response = send_reliable_submission(my_tx_payment_signed, client)

    return tx_response


def cancel_offer(client: JsonRpcClient, from_wallet: Wallet, sequence: int) -> Response:
    """
    Cancel order

    :param client: xrpl Client
    :type client: JsonRpcClient

    :param from_wallet: XRPL Wallet
    :type from_wallet: Wallet

    :param sequence: The sequence number (or Ticket number) of a previous OfferCreate transaction.
    :type sequence: int

    :return: Result of order canceling attempt
    :rtype: Response
    """

    offer_create = OfferCancel(
        account=from_wallet.classic_address,
        offer_sequence=sequence
    )

    my_tx_payment_signed = safe_sign_and_autofill_transaction(offer_create, from_wallet, client)
    tx_response = send_reliable_submission(my_tx_payment_signed, client)

    return tx_response
