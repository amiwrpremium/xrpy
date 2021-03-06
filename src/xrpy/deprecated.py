import warnings
from deprecation import deprecated

from typing import Union


from xrpl.account import get_account_info as xrpl_get_account_info

from xrpl.clients import JsonRpcClient, WebsocketClient
from xrpl.wallet import generate_faucet_wallet, Wallet

from xrpl.utils import xrp_to_drops

from xrpl.models.transactions import Payment, TrustSet, TrustSetFlag, OfferCreate, OfferCancel, OfferCreateFlag, \
    Transaction
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.models.response import Response

from xrpl.models.requests import BookOffers, AccountLines, AccountOffers
from xrpl.models.currencies import XRP

from xrpl.transaction import safe_sign_and_autofill_transaction, send_reliable_submission


from .main import __version__


__deprecated_in__ = "0.2.0"
__remove_in__ = "1.0.0"


@deprecated(
    deprecated_in=__deprecated_in__, removed_in=__remove_in__,
    current_version=__version__, details='Use `XRPY class, create_wallet method` instead.'
)
def create_wallet(client: JsonRpcClient) -> Wallet:
    """
    Create a wallet

    :param client: xrpl Client
    :type client: JsonRpcClient, WebsocketClient

    :return: XRPL Wallet
    :rtype: Wallet
    """

    warnings.warn("This function is deprecated. Use `XRPY class, create_wallet method` instead.", DeprecationWarning)

    _wallet = generate_faucet_wallet(client)
    return _wallet


@deprecated(
    deprecated_in=__deprecated_in__, removed_in=__remove_in__,
    current_version=__version__, details='Use `XRPY class, transfer_xrp method` instead.'
)
def send_transaction(client: Union[JsonRpcClient, WebsocketClient], from_wallet: Wallet, amount: Union[int, float],
                     destination: str) -> Response:
    """
    Send a transaction

    :param client: xrpl Client
    :type client: JsonRpcClient, WebsocketClient

    :param from_wallet: XRPL Wallet
    :type from_wallet: Wallet

    :param amount: Amount to send
    :type amount: Union[int, float]

    :param destination: Destination address
    :type destination: str

    :return: Result of transaction sending attempt
    :rtype: Response
    """

    warnings.warn("This function is deprecated. Use `XRPY class, transfer_xrp method` instead.", DeprecationWarning)

    payment = Payment(
        account=from_wallet.classic_address,
        amount=xrp_to_drops(amount),
        destination=destination,
    )

    payment_signed = safe_sign_and_autofill_transaction(payment, from_wallet, client)
    response = send_reliable_submission(payment_signed, client)

    return response


@deprecated(
    deprecated_in=__deprecated_in__, removed_in=__remove_in__,
    current_version=__version__, details='Use `XRPY class, set_trust_line method` instead.'
)
def set_trust_line(client: Union[JsonRpcClient, WebsocketClient], from_wallet: Wallet,
                   currency: str, value: str, issuer: str) -> Response:
    """
    Create a trust line

    :param client: xrpl Client
    :type client: JsonRpcClient, WebsocketClient

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

    warnings.warn("This function is deprecated. Use `XRPY class, set_trust_line method` instead.", DeprecationWarning)

    trust_set = TrustSet(
        account=from_wallet.classic_address,
        limit_amount=IssuedCurrencyAmount(
            currency=currency.upper(),
            value=value,
            issuer=issuer,
        ),
        flags=TrustSetFlag.TF_SET_NO_RIPPLE
    )

    trust_set_signed = safe_sign_and_autofill_transaction(trust_set, from_wallet, client)
    response = send_reliable_submission(trust_set_signed, client)

    return response


@deprecated(
    deprecated_in=__deprecated_in__, removed_in=__remove_in__,
    current_version=__version__, details='Use `XRPY class, create_buy_offer method` instead.'
)
def create_offer_buy(client: Union[JsonRpcClient, WebsocketClient], from_wallet: Wallet,
                     taker_gets_xrp: Union[float, int],
                     taker_pays_currency: str, taker_pays_value: str, taker_pays_issuer: str, _type: str) -> Response:
    """
    Place Order

    :param client: xrpl Client
    :type client: JsonRpcClient, WebsocketClient

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

    :param _type: Offer type (market or limit)
    :type _type: str

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

    warnings.warn("This function is deprecated. Use `XRPY class, create_offer_buy method` instead.", DeprecationWarning)

    offer_create = OfferCreate(
        account=from_wallet.classic_address,
        taker_gets=xrp_to_drops(taker_gets_xrp),
        taker_pays=IssuedCurrencyAmount(
            currency=taker_pays_currency,
            value=taker_pays_value,
            issuer=taker_pays_issuer,
        ),
        flags=OfferCreateFlag.TF_SELL if _type.lower() == 'market' else 0
    )

    offer_create_signed = safe_sign_and_autofill_transaction(offer_create, from_wallet, client)
    response = send_reliable_submission(offer_create_signed, client)

    return response


@deprecated(
    deprecated_in=__deprecated_in__, removed_in=__remove_in__,
    current_version=__version__, details='Use `XRPY class, create_sell_offer method` instead.'
)
def create_offer_sell(client: Union[JsonRpcClient, WebsocketClient], from_wallet: Wallet,
                      taker_pays_xrp: Union[float, int],
                      taker_gets_currency: str, taker_gets_value: str, taker_gets_issuer: str,
                      _type: str) -> Response:
    """
    Place Order

    :param client: xrpl Client
    :type client: JsonRpcClient, WebsocketClient

    :param from_wallet: XRPL Wallet
    :type from_wallet: Wallet

    :param taker_pays_xrp: amount in xrp for taker pays
    :type taker_pays_xrp: int

    :param taker_gets_currency: Currency
    :type taker_gets_currency: str

    :param taker_gets_value: Value
    :type taker_gets_value: str

    :param taker_gets_issuer: Issuer
    :type taker_gets_issuer: str

    :param _type: Offer type (market or limit)
    :type _type: str

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

    warnings.warn("This function is deprecated. Use `XRPY class, create_offer_sell method` instead.", DeprecationWarning)

    offer_create = OfferCreate(
        account=from_wallet.classic_address,
        taker_gets=IssuedCurrencyAmount(
            currency=taker_gets_currency,
            value=taker_gets_value,
            issuer=taker_gets_issuer,
        ),
        taker_pays=xrp_to_drops(taker_pays_xrp),
        flags=OfferCreateFlag.TF_SELL if _type.lower() == 'market' else 0
    )

    offer_create_signed = safe_sign_and_autofill_transaction(offer_create, from_wallet, client)
    response = send_reliable_submission(offer_create_signed, client)

    return response


@deprecated(
    deprecated_in=__deprecated_in__, removed_in=__remove_in__,
    current_version=__version__, details='Use `XRPY class, cancel_offer method` instead.'
)
def cancel_offer(client: Union[JsonRpcClient, WebsocketClient], from_wallet: Wallet, sequence: int) -> Response:
    """
    Cancel order

    :param client: xrpl Client
    :type client: JsonRpcClient, WebsocketClient

    :param from_wallet: XRPL Wallet
    :type from_wallet: Wallet

    :param sequence: The sequence number (or Ticket number) of a previous OfferCreate transaction.
    :type sequence: int

    :return: Result of order canceling attempt
    :rtype: Response
    """

    warnings.warn("This function is deprecated. Use `XRPY class, cancel_offer method` instead.", DeprecationWarning)

    offer_create = OfferCancel(
        account=from_wallet.classic_address,
        offer_sequence=sequence
    )

    offer_create_signed = safe_sign_and_autofill_transaction(offer_create, from_wallet, client)
    response = send_reliable_submission(offer_create_signed, client)

    return response


@deprecated(
    deprecated_in=__deprecated_in__, removed_in=__remove_in__,
    current_version=__version__, details='Use `XRPY class, get_account_info method` instead.'
)
def get_account_info(client: Union[JsonRpcClient, WebsocketClient], address: str) -> Response:
    """
    Get Account Info

    :param client: xrpl Client
    :type client: JsonRpcClient, WebsocketClient

    :param address: Wallet address
    :type address: str

    :return: Account info
    :rtype: Response
    """

    warnings.warn("This function is deprecated. Use `XRPY class, get_account_info method` instead.", DeprecationWarning)

    acc_info = xrpl_get_account_info(address, client)

    return acc_info


@deprecated(
    deprecated_in=__deprecated_in__, removed_in=__remove_in__,
    current_version=__version__, details='Use `XRPY class, get_account_trustlines method` instead.'
)
def get_account_trustlines(client: Union[JsonRpcClient, WebsocketClient], address: str) -> Response:
    """
    Get Account Trustlines

    :param client: xrpl Client
    :type client: JsonRpcClient, WebsocketClient

    :param address: Wallet address
    :type address: str

    :return: Account Trustlines
    :rtype: Response
    """

    warnings.warn("This function is deprecated. Use `XRPY class, get_account_trustlines method` instead.", DeprecationWarning)

    account_lines = AccountLines(
        account=address,
    )
    account_lines_req = client.request(account_lines)

    return account_lines_req


@deprecated(
    deprecated_in=__deprecated_in__, removed_in=__remove_in__,
    current_version=__version__, details='Use `XRPY class, get_account_offers method` instead.'
)
def get_account_offers(client: Union[JsonRpcClient, WebsocketClient], address: str) -> Response:
    """
    Get Account Trustlines

    :param client: xrpl Client
    :type client: JsonRpcClient, WebsocketClient

    :param address: Wallet address
    :type address: str

    :return: Account Trustlines
    :rtype: Response
    """

    warnings.warn("This function is deprecated. Use `XRPY class, get_account_offers method` instead.", DeprecationWarning)

    account_offers = AccountOffers(
        account=address,
    )
    account_offers_req = client.request(account_offers)

    return account_offers_req


@deprecated(
    deprecated_in=__deprecated_in__, removed_in=__remove_in__,
    current_version=__version__, details='Use `XRPY class, order_book_sell method` instead.'
)
def order_book_sell(client: Union[JsonRpcClient, WebsocketClient], classic_address: str,
                    taker_pays_currency: Union[str, XRP], taker_pays_issuer: str) -> Response:
    """
    Get Orderbook

    :param client: xrpl Client
    :type client: JsonRpcClient, WebsocketClient

    :param classic_address: Wallet address
    :type classic_address: str

    :param taker_pays_currency: Currency
    :type taker_pays_currency: str

    :param taker_pays_issuer: Issuer
    :type taker_pays_issuer: str

    :return: Result of order placing attempt
    :rtype: Response

    """

    warnings.warn("This function is deprecated. Use `XRPY class, order_book_sell method` instead.", DeprecationWarning)

    book_offers = BookOffers(
        taker=classic_address,
        taker_gets=IssuedCurrencyAmount(
            currency=taker_pays_currency,
            value='0',
            issuer=taker_pays_issuer,
        ),
        taker_pays=XRP(),
    )

    book_offers_req = client.request(book_offers)

    return book_offers_req


@deprecated(
    deprecated_in=__deprecated_in__, removed_in=__remove_in__,
    current_version=__version__, details='Use `XRPY class, order_book_buy method` instead.'
)
def order_book_buy(client: Union[JsonRpcClient, WebsocketClient], classic_address: str,
                   taker_pays_currency: Union[str, XRP], taker_pays_issuer: str) -> Response:
    """
    Get Orderbook

    :param client: xrpl Client
    :type client: JsonRpcClient, WebsocketClient

    :param classic_address: Wallet address
    :type classic_address: str

    :param taker_pays_currency: Currency
    :type taker_pays_currency: str

    :param taker_pays_issuer: Issuer
    :type taker_pays_issuer: str

    :return: Result of order placing attempt
    :rtype: Response
    """

    warnings.warn("This function is deprecated. Use `XRPY class, order_book_buy method` instead.", DeprecationWarning)

    book_offers = BookOffers(
        taker=classic_address,
        taker_gets=XRP(),
        taker_pays=IssuedCurrencyAmount(
            currency=taker_pays_currency,
            value='0',
            issuer=taker_pays_issuer,
        ),
    )

    book_offers_req = client.request(book_offers)

    return book_offers_req


@deprecated(
    deprecated_in=__deprecated_in__, removed_in=__remove_in__,
    current_version=__version__, details='Use `XRPY class, get_reserved_balance method` instead.'
)
def get_reserved_balance(client: Union[JsonRpcClient, WebsocketClient], address: str,
                         include_wallet_reserve: bool = False) -> int:
    """
    Get Reserved Balance

    :param client: xrpl Client
    :type client: JsonRpcClient, WebsocketClient

    :param address: Wallet address
    :type address: str

    :param include_wallet_reserve: Include Wallet Reserve (+10 for wallet reserve) (default: False)
    :type include_wallet_reserve: bool

    :return: Reserved Balance
    :rtype: Response
    """

    warnings.warn("This function is deprecated. Use `XRPY class, get_reserved_balance method` instead.", DeprecationWarning)

    trust_lines = get_account_trustlines(client, address)

    result = 2 * len(trust_lines.result.get('lines', 0))
    if include_wallet_reserve is True:
        result += 10

    return result


@deprecated(
    deprecated_in=__deprecated_in__, removed_in=__remove_in__,
    current_version=__version__, details='Use `XRPY class, get_reserved_balance method` instead.'
)
def get_balance(client: Union[JsonRpcClient, WebsocketClient], address: str,
                include_wallet_reserve: bool = True) -> Union[float, int]:
    """
    Get Balance in drops

    :param client: xrpl Client
    :type client: JsonRpcClient, WebsocketClient

    :param address: Wallet address
    :type address: str

    :param include_wallet_reserve: Include Wallet Reserve (+10 for wallet reserve) (default: False)
    :type include_wallet_reserve: bool

    :return: Balance in drops
    :rtype: Response
    """

    warnings.warn("This function is deprecated. Use `XRPY class, get_balance method` instead.", DeprecationWarning)

    account_info = xrpl_get_account_info(address, client)

    result = account_info.result.get('account_data', {}).get('Balance', 0) or 0

    if include_wallet_reserve is False:
        reserved = get_reserved_balance(client, address, True)
        result -= reserved

    return result
