from typing import Union, Optional


from xrpl.account import get_account_info as xrpl_get_account_info

from xrpl.clients import JsonRpcClient, WebsocketClient
from xrpl.wallet import generate_faucet_wallet, Wallet

from xrpl.utils import xrp_to_drops

from xrpl.models.transactions import Payment, TrustSet, TrustSetFlag, OfferCreate, OfferCancel, OfferCreateFlag, \
    Transaction, AccountDelete
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.models.response import Response

from xrpl.models.requests import BookOffers, AccountLines, AccountOffers
from xrpl.models.currencies import XRP

from xrpl.transaction import safe_sign_and_autofill_transaction, send_reliable_submission


__version__ = '0.2.0'


__all__ = [
    'XRPY',
    'JsonRpcClient',
    'WebsocketClient',
    'XRP',
    'Wallet',
]


class XRPY:
    """
    XRPY is a wrapper for the XRPL API.
    """

    def __init__(self, client: Optional[Union[JsonRpcClient, WebsocketClient, str]] = None):
        """
        XRPY is a wrapper for the XRPL API.

        You can initialize XRPY with a client, or you can initialize it with a url string.

        :param client: XRPL client
        :type client: Optional[Union[JsonRpcClient, WebsocketClient, str]]

        :raises TypeError: If client is not a JsonRpcClient or WebsocketClient

        :return: XRPY
        """

        if client is None:
            client = JsonRpcClient('https://xrplcluster.com')
        elif type(client) is str:
            client = JsonRpcClient(client)
        elif type(client) is JsonRpcClient or type(client) is WebsocketClient:
            client = client
        else:
            raise Exception(f'Invalid client type: {type(client)}')

        self._client = client

    def set_client(self, client: Union[JsonRpcClient, WebsocketClient]) -> None:
        """
        Set the client for the XRPY instance.

        :param client: XRPL client
        :type client: Union[JsonRpcClient, WebsocketClient]

        :return: None
        """

        self._client = client

    def _sign_and_send(self, transaction: Transaction, from_wallet: Wallet) -> Response:
        """
        Sign and send a transaction

        :param transaction: Transaction to sign and send
        :type transaction: Transaction

        :param from_wallet: Wallet to sign the transaction with
        :type from_wallet: Wallet

        :return: Response
        :rtype: Response
        """

        safe_signed = safe_sign_and_autofill_transaction(transaction, from_wallet, self._client)
        response = send_reliable_submission(safe_signed, self._client)

        return response

    def create_wallet(self, wallet: Optional[Wallet] = None, debug: bool = False) -> Wallet:
        """
        Create a wallet

        :param wallet: A wallet to use for the creation process. If None, a new wallet will be created.
        :type wallet: Optional[Wallet]

        :param debug: Whether to print debug information as it creates the wallet.
        :type debug: bool

        :return: XRPL Wallet
        :rtype: Wallet
        """

        _wallet = generate_faucet_wallet(self._client, wallet, debug)
        return _wallet

    def transfer_xrp(
            self, from_wallet: Wallet, amount: Union[int, float], destination: str
    ) -> Response:
        """
        Transfer XRP

        :param from_wallet: XRPL Wallet
        :type from_wallet: Wallet

        :param amount: Amount to send
        :type amount: Union[int, float]

        :param destination: Destination address
        :type destination: str

        :return: Result of transaction sending attempt
        :rtype: Response
        """

        payment = Payment(
            account=from_wallet.classic_address,
            amount=xrp_to_drops(amount),
            destination=destination,
        )

        response = self._sign_and_send(payment, from_wallet)
        return response
    
    def transfer_token(
            self, from_wallet: Wallet, currency: str, amount: Union[int, float], destination: str, issuer: str
    ) -> Response:
        """
        Transfer XRP

        :param from_wallet: XRPL Wallet
        :type from_wallet: Wallet
        
        :param currency: Currency to send
        :type currency: str

        :param amount: Amount to send
        :type amount: Union[int, float]

        :param destination: Destination address
        :type destination: str

        :param issuer: Issuer address
        :type issuer: str

        :return: Result of transaction sending attempt
        :rtype: Response
        """

        payment = Payment(
            account=from_wallet.classic_address,
            amount=IssuedCurrencyAmount(
                currency=currency,
                value=amount,
                issuer=issuer,
            ),
            destination=destination,
        )

        response = self._sign_and_send(payment, from_wallet)
        return response

    def set_trust_line(self, from_wallet: Wallet, currency: str, value: str, issuer: str) -> Response:
        """
        Create a trust line

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

        response = self._sign_and_send(trust_set, from_wallet)
        return response

    def create_buy_offer(
            self, from_wallet: Wallet, taker_gets_xrp: Union[float, int],
            taker_pays_currency: str, taker_pays_value: str, taker_pays_issuer: str,
            _type: str
    ) -> Response:
        """
        Place Order

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
        """

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

        response = self._sign_and_send(offer_create, from_wallet)
        return response

    def create_sell_offer(
            self, from_wallet: Wallet, taker_pays_xrp: Union[float, int],
            taker_gets_currency: str, taker_gets_value: str, taker_gets_issuer: str,
            _type: str
    ) -> Response:
        """
        Place Order

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
        """

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

        response = self._sign_and_send(offer_create, from_wallet)
        return response

    def cancel_offer(self, from_wallet: Wallet, offer_sequence: int) -> Response:
        """
        Cancel order

        :param from_wallet: XRPL Wallet
        :type from_wallet: Wallet

        :param offer_sequence: The sequence number (or Ticket number) of a previous OfferCreate transaction.
        :type offer_sequence: int

        :return: Result of order canceling attempt
        :rtype: Response
        """

        offer_create = OfferCancel(
            account=from_wallet.classic_address,
            offer_sequence=offer_sequence
        )

        response = self._sign_and_send(offer_create, from_wallet)
        return response

    def get_account_info(self, address: str) -> Response:
        """
        Get Account Info

        :param address: Wallet address
        :type address: str

        :return: Account info
        :rtype: Response
        """

        acc_info = xrpl_get_account_info(address, self._client)

        return acc_info

    def get_account_trustlines(self, address: str) -> Response:
        """
        Get Account Trustlines

        :param address: Wallet address
        :type address: str

        :return: Account Trustlines
        :rtype: Response
        """

        account_lines = AccountLines(
            account=address,
        )
        account_lines_req = self._client.request(account_lines)

        return account_lines_req

    def get_account_offers(self, address: str) -> Response:
        """
        Get Account Trustlines

        :param address: Wallet address
        :type address: str

        :return: Account Trustlines
        :rtype: Response
        """

        account_offers = AccountOffers(
            account=address,
        )
        account_offers_req = self._client.request(account_offers)

        return account_offers_req

    def order_book_sell(
            self, classic_address: str, taker_pays_currency: Union[str, XRP], taker_pays_issuer: str
    ) -> Response:
        """
        Get Orderbook

        :param classic_address: Wallet address
        :type classic_address: str

        :param taker_pays_currency: Currency
        :type taker_pays_currency: str

        :param taker_pays_issuer: Issuer
        :type taker_pays_issuer: str

        :return: Result of order placing attempt
        :rtype: Response

        """

        book_offers = BookOffers(
            taker=classic_address,
            taker_gets=IssuedCurrencyAmount(
                currency=taker_pays_currency,
                value='0',
                issuer=taker_pays_issuer,
            ),
            taker_pays=XRP(),
        )

        book_offers_req = self._client.request(book_offers)

        return book_offers_req

    def order_book_buy(
            self, classic_address: str, taker_pays_currency: Union[str, XRP], taker_pays_issuer: str
    ) -> Response:
        """
        Get Orderbook

        :param classic_address: Wallet address
        :type classic_address: str

        :param taker_pays_currency: Currency
        :type taker_pays_currency: str

        :param taker_pays_issuer: Issuer
        :type taker_pays_issuer: str

        :return: Result of order placing attempt
        :rtype: Response
        """

        book_offers = BookOffers(
            taker=classic_address,
            taker_gets=XRP(),
            taker_pays=IssuedCurrencyAmount(
                currency=taker_pays_currency,
                value='0',
                issuer=taker_pays_issuer,
            ),
        )

        book_offers_req = self._client.request(book_offers)

        return book_offers_req

    def get_reserved_balance(self, address: str, include_wallet_reserve: bool = False) -> int:
        """
        Get Reserved Balance

        :param address: Wallet address
        :type address: str

        :param include_wallet_reserve: Include Wallet Reserve (+10 for wallet reserve) (default: False)
        :type include_wallet_reserve: bool

        :return: Reserved Balance
        :rtype: Response
        """

        trust_lines = self.get_account_trustlines(address)

        result = 2 * len(trust_lines.result.get('lines', 0))
        if include_wallet_reserve is True:
            result += 10

        return result

    def get_balance(self, address: str, include_wallet_reserve: bool = True) -> Union[float, int]:
        """
        Get Balance in drops

        :param address: Wallet address
        :type address: str

        :param include_wallet_reserve: Include Wallet Reserve (+10 for wallet reserve) (default: False)
        :type include_wallet_reserve: bool

        :return: Balance in drops
        :rtype: Response
        """

        account_info = xrpl_get_account_info(address, self._client)

        result = float(account_info.result.get('account_data', {}).get('Balance', 0)) or 0

        if include_wallet_reserve is False:
            reserved = self.get_reserved_balance(address, True)
            result -= reserved

        return float(result)

    def __str__(self):
        return f'XRPY Client: {self._client}, Version: {__version__}'

    def __repr__(self):
        return self.__str__()
