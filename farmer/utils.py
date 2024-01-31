from logging import Logger

def handle_order_execution_results_hl(order_result: dict, logger: Logger) -> dict:
    """
    Function gets a dict with results of operation execution and returns either it was successfull or not. It also produces logging
    """

    if order_result["status"] == "ok":
        for status in order_result["response"]["data"]["statuses"]:
            try:
                filled = status["filled"]
                logger.info(f'Order #{filled["oid"]} filled {filled["totalSz"]} @{filled["avgPx"]}')
                return {'filled': True, "status": 0}
                
            except KeyError:
                if "resting" in status:
                    resting = status['resting']
                    logger.info(f"Order #{resting['oid']} is open")
                    return {"filled": False, "status": 0}
                else:
                    logger.error(status)
                    return {"status": 1}
        else:
            return {"status": 1}