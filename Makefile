.PHONY: me him her yourself a sandwich all

me:
	@echo -n '';

him:
	@echo -n '';

her:
	@echo -n '';

yourself:
	@echo -n '';

a:
	@echo -n '';

sandwich:
	@[ `id -u` -eq 0 ] && echo "Okay." || echo "What? Make it yourself!"

all:
	@echo -n '';
