"use client";

import {
  Box,
  Grid,
  GridItem,
  Heading,
  Icon,
  Stack,
  Text,
  useColorModeValue
} from "@chakra-ui/react";
import { FiActivity, FiLayers, FiLock, FiMonitor } from "react-icons/fi";

const features = [
  {
    title: "Composable runbooks",
    description:
      "Design deterministic or adaptive agent flows using reusable templates tailored to your teams.",
    icon: FiLayers
  },
  {
    title: "Observability-first",
    description:
      "Capture every decision with structured telemetry, enabling faster incident response and RCA.",
    icon: FiMonitor
  },
  {
    title: "Zero-trust security",
    description:
      "Rotate credentials automatically, apply network segmentation, and enforce granular approvals.",
    icon: FiLock
  },
  {
    title: "Autonomous optimization",
    description:
      "Deploy guardrails that continuously tune prompts and models for quality, cost, and safety.",
    icon: FiActivity
  }
];

export function FeatureGrid() {
  const cardBg = useColorModeValue("whiteAlpha.200", "whiteAlpha.100");
  const border = useColorModeValue("whiteAlpha.300", "whiteAlpha.200");

  return (
    <Stack as="section" spacing={12} py={{ base: 16, lg: 24 }}>
      <Stack spacing={4} textAlign="center" maxW="3xl" mx="auto">
        <Heading size="2xl">Ship responsibly at scale</Heading>
        <Text fontSize="lg" color="whiteAlpha.700">
          The Agent Orchestration Platform combines security tooling with Saas UI components
          to help product teams launch workflows that are as compliant as they are fast.
        </Text>
      </Stack>
      <Grid
        templateColumns={{ base: "repeat(1, 1fr)", md: "repeat(2, 1fr)" }}
        gap={{ base: 6, lg: 8 }}
      >
        {features.map((feature) => (
          <GridItem key={feature.title}>
            <Stack
              h="full"
              spacing={4}
              p={8}
              borderRadius="2xl"
              bg={cardBg}
              border="1px solid"
              borderColor={border}
              backdropFilter="auto"
              backdropBlur="18px"
            >
              <Box
                w={12}
                h={12}
                borderRadius="full"
                display="flex"
                alignItems="center"
                justifyContent="center"
                bg="brand.500"
                color="white"
                boxShadow="0 10px 30px rgba(59, 130, 246, 0.45)"
              >
                <Icon as={feature.icon} boxSize={6} />
              </Box>
              <Heading size="md">{feature.title}</Heading>
              <Text color="whiteAlpha.700">{feature.description}</Text>
            </Stack>
          </GridItem>
        ))}
      </Grid>
    </Stack>
  );
}
