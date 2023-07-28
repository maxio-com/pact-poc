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
6. Check out `add bpp to consumer`. Regenerate pacts. Verify that provider fails now.
7. Check out `add test setup to provider`. Add
   `--provider-states-setup-url=http://localhost:5000/provider_states_setup/` to `pact-verifier` incantation. Verify that the provider succeeds now.
8. Check out `add async messaging contract`. Run `pytest test_messages.py` in `./consumer`. Publish `maxiocoreasync-advancedbillingasync.json`. Provider verification now handled by running `pytest` in `./provider`.
   - Note that here it _could_ be nice to have both async message and REST contracts labeled by same consumer / provider
     pairs. This is possible with newer Pact contract schema, v4. However, this new schema not yet supported by
     pact-broker (for UI) or python SDK (for verification). First problem can throw $ at - commercial pact-flow displays
     v4 contracts. Second problem can throw hours at - we can submit PRs to pact python SDK to support v4 specification.
