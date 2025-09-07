public function getBaseBasketPriceForPaymentCostCalc($oBasket)
    {
        $dBasketPrice = 0;
        $iRules = $this->oxpayments__oxaddsumrules->value;

        // products brutto price
        if (!$iRules || ($iRules & self::PAYMENT_ADDSUMRULE_ALLGOODS)) {
            $dBasketPrice += $oBasket->getProductsPrice()->getSum($oBasket->isCalculationModeNetto());
        }

        // discounts
        if ((!$iRules || ($iRules & self::PAYMENT_ADDSUMRULE_DISCOUNTS)) &&
            ($oCosts = $oBasket->getTotalDiscount())
        ) {
            $dBasketPrice -= $oCosts->getPrice();
        }

        // vouchers
        if (!$iRules || ($iRules & self::PAYMENT_ADDSUMRULE_VOUCHERS)) {
            $dBasketPrice -= $oBasket->getVoucherDiscValue();
        }

        // delivery
        if ((!$iRules || ($iRules & self::PAYMENT_ADDSUMRULE_SHIPCOSTS)) &&
            ($oCosts = $oBasket->getCosts('oxdelivery'))
        ) {
            if ($oBasket->isCalculationModeNetto()) {
                $dBasketPrice += $oCosts->getNettoPrice();
            } else {
                $dBasketPrice += $oCosts->getBruttoPrice();
            }
        }

        // wrapping
        if (($iRules & self::PAYMENT_ADDSUMRULE_GIFTS) &&
            ($oCosts = $oBasket->getCosts('oxwrapping'))
        ) {
            if ($oBasket->isCalculationModeNetto()) {
                $dBasketPrice += $oCosts->getNettoPrice();
            } else {
                $dBasketPrice += $oCosts->getBruttoPrice();
            }
        }

        // gift card
        if (($iRules & self::PAYMENT_ADDSUMRULE_GIFTS) &&
            ($oCosts = $oBasket->getCosts('oxgiftcard'))
        ) {
            if ($oBasket->isCalculationModeNetto()) {
                $dBasketPrice += $oCosts->getNettoPrice();
            } else {
                $dBasketPrice += $oCosts->getBruttoPrice();
            }
        }

        return $dBasketPrice;
    }