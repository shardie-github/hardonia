vendor-packs:
	@if [ -z "$(TAG)" ]; then echo "Usage: make vendor-packs TAG=v1.2.3"; exit 1; fi
	@./scripts/vendor-packs.sh "$(TAG)"
