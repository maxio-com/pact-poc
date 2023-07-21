### Pact proof-of-concept

Instructions
1. Run Pact Broker on port 9292
2. Set up python envs for both consumer and provider, `pip install -r requirements.txt`
3. Starting with `init` commit, run `pytest` in `./consumer/` to generate contracts - will populate `pacts/` folder
4. Publish consumer contracts to broker with `pact-broker publish pacts/maxiocore-advancedbilling.json --broker-base-url http://localhost:9292`
   - Here adding `--consumer-app-version $(git rev-parse --short HEAD)` may be of interest
5. Verify provider app
   - Need to start the local provider Flask app by running `provider/app.py` 
   - Command is `pact-verifier --provider-base-url=http://localhost:5000 --pact-url=http://localhost:9292/pacts/provider/AdvancedBilling/consumer/MaxioCore/latest`
   - Add `-a $(git rev-parse --short HEAD) -r` to publish verification results to broker
