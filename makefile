.PHONY: dev docker worker

dev:
	npm run dev

worker:
	npx inngest-cli@latest dev -u http://localhost:3000/api/inngest

docker:
	docker compose up -d
