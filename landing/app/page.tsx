import { Container, Divider, Stack } from "@chakra-ui/react";
import { FeatureGrid } from "@/components/FeatureGrid";
import { Footer } from "@/components/Footer";
import { Hero } from "@/components/Hero";
import { Pricing } from "@/components/Pricing";
import { Testimonials } from "@/components/Testimonials";

export default function Page() {
  return (
    <Container maxW="6xl" px={{ base: 6, md: 10 }}>
      <Stack spacing={{ base: 16, lg: 24 }}>
        <Hero />
        <Divider borderColor="whiteAlpha.200" />
        <FeatureGrid />
        <Divider borderColor="whiteAlpha.200" />
        <Testimonials />
        <Divider borderColor="whiteAlpha.200" />
        <Pricing />
        <Footer />
      </Stack>
    </Container>
  );
}
