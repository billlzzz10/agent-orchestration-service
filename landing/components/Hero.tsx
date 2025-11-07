"use client";

import { Button, ButtonGroup, Flex, Heading, Icon, Stack, Text } from "@chakra-ui/react";
import { motion } from "framer-motion";
import { FiArrowRight } from "react-icons/fi";

const MotionStack = motion(Stack);

export function Hero() {
  return (
    <Flex
      as="section"
      direction={{ base: "column", lg: "row" }}
      align={{ base: "flex-start", lg: "center" }}
      gap={{ base: 10, lg: 16 }}
      py={{ base: 20, lg: 32 }}
    >
      <MotionStack
        spacing={{ base: 6, lg: 8 }}
        maxW="3xl"
        initial={{ opacity: 0, y: 32 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
      >
        <Text
          textTransform="uppercase"
          color="brand.400"
          fontWeight="semibold"
          letterSpacing="widest"
        >
          Orchestrate secure AI operations
        </Text>
        <Heading
          as="h1"
          size="3xl"
          fontWeight="extrabold"
          lineHeight={1.1}
          textShadow="0 12px 32px rgba(37, 99, 235, 0.35)"
        >
          Launch production-grade agent workflows in minutes
        </Heading>
        <Text fontSize="lg" color="whiteAlpha.800" maxW="2xl">
          Automate complex business processes with compliant, auditable agent pipelines.
          Saas UI provides the building blocks—our platform delivers the governance,
          observability, and security you need to scale with confidence.
        </Text>
        <ButtonGroup spacing={4} flexWrap="wrap">
          <Button
            as="a"
            href="/docs/getting-started"
            size="lg"
            colorScheme="brand"
            rightIcon={<Icon as={FiArrowRight} />}
          >
            Launch sandbox
          </Button>
          <Button
            as="a"
            href="/contact"
            size="lg"
            variant="outline"
            borderColor="whiteAlpha.400"
            _hover={{ borderColor: "whiteAlpha.700", bg: "whiteAlpha.200" }}
          >
            Book a demo
          </Button>
        </ButtonGroup>
      </MotionStack>
      <Flex
        flex="1"
        w="full"
        minH={{ base: 60, md: 80 }}
        borderRadius="3xl"
        bgGradient="linear(135deg, rgba(59, 130, 246, 0.8), rgba(14, 116, 144, 0.6))"
        boxShadow="xl"
        position="relative"
        overflow="hidden"
        _after={{
          content: '""',
          position: "absolute",
          inset: "4",
          borderRadius: "2xl",
          border: "1px solid",
          borderColor: "whiteAlpha.300"
        }}
      >
        <Stack
          spacing={6}
          p={{ base: 8, md: 12 }}
          justify="center"
          color="whiteAlpha.900"
        >
          <Heading size="lg">Enterprise-grade controls</Heading>
          <Text color="whiteAlpha.800">
            Built-in encryption, policy enforcement, and environment isolation ensure your
            teams ship responsibly from day zero.
          </Text>
          <Text fontSize="sm" color="whiteAlpha.700">
            SOC2-ready • Granular RBAC • Continuous compliance monitoring
          </Text>
        </Stack>
      </Flex>
    </Flex>
  );
}
