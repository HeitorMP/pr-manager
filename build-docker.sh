#!/bin/bash
# Build and run script for PR Manager

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🐳 Building PR Manager Docker image...${NC}"
docker build -t pr-manager-tui .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Build successful!${NC}"
    echo -e "${YELLOW}📋 To run the application:${NC}"
    echo ""
    echo "  docker run -it --rm -e GITHUB_TOKEN=your_token -e GITHUB_ORG=your_org pr-manager-tui"
    echo ""
    echo -e "${YELLOW}Or using docker-compose:${NC}"
    echo ""
    echo "  docker-compose run --rm pr-manager"
    echo ""
else
    echo "❌ Build failed!"
    exit 1
fi
