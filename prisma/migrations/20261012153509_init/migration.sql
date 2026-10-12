-- CreateEnum
CREATE TYPE "Role" AS ENUM ('ADMIN', 'OPERATOR', 'VIEWER');

-- CreateEnum
CREATE TYPE "StationKind" AS ENUM ('PHYSICAL', 'SIMULATED');

-- CreateEnum
CREATE TYPE "ReadingFlag" AS ENUM ('OK', 'SUSPECT', 'BAD');

-- CreateEnum
CREATE TYPE "SampleSource" AS ENUM ('LAB', 'FIELD_KIT');

-- CreateEnum
CREATE TYPE "ResultQualifier" AS ENUM ('EQUAL', 'LESS_THAN', 'GREATER_THAN');

-- CreateEnum
CREATE TYPE "AlertSeverity" AS ENUM ('LOW', 'MEDIUM', 'HIGH');

-- CreateEnum
CREATE TYPE "AlertStatus" AS ENUM ('OPEN', 'ACKNOWLEDGED', 'RESOLVED');

-- CreateTable
CREATE TABLE "Organisation" (
    "id" UUID NOT NULL,
    "name" TEXT NOT NULL,
    "createdAt" TIMESTAMPTZ(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Organisation_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "User" (
    "id" UUID NOT NULL,
    "organisationId" UUID NOT NULL,
    "name" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "passwordHash" TEXT,
    "role" "Role" NOT NULL DEFAULT 'VIEWER',
    "createdAt" TIMESTAMPTZ(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "User_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Site" (
    "id" UUID NOT NULL,
    "organisationId" UUID NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,
    "latitude" DECIMAL(9,6),
    "longitude" DECIMAL(9,6),
    "createdAt" TIMESTAMPTZ(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Site_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Station" (
    "id" UUID NOT NULL,
    "siteId" UUID NOT NULL,
    "name" TEXT NOT NULL,
    "kind" "StationKind" NOT NULL DEFAULT 'PHYSICAL',
    "latitude" DECIMAL(9,6),
    "longitude" DECIMAL(9,6),
    "installedAt" TIMESTAMPTZ(6),
    "retiredAt" TIMESTAMPTZ(6),
    "createdAt" TIMESTAMPTZ(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Station_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Sensor" (
    "id" UUID NOT NULL,
    "serialNumber" TEXT NOT NULL,
    "manufacturer" TEXT,
    "model" TEXT,
    "notes" TEXT,

    CONSTRAINT "Sensor_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "SensorInstallation" (
    "id" UUID NOT NULL,
    "sensorId" UUID NOT NULL,
    "stationId" UUID NOT NULL,
    "depthM" DECIMAL(6,2),
    "installedAt" TIMESTAMPTZ(6) NOT NULL,
    "removedAt" TIMESTAMPTZ(6),

    CONSTRAINT "SensorInstallation_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Parameter" (
    "id" SERIAL NOT NULL,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "unit" TEXT NOT NULL,

    CONSTRAINT "Parameter_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Standard" (
    "id" SERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "source" TEXT,

    CONSTRAINT "Standard_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Limit" (
    "id" SERIAL NOT NULL,
    "standardId" INTEGER NOT NULL,
    "parameterId" INTEGER NOT NULL,
    "minValue" DOUBLE PRECISION,
    "maxValue" DOUBLE PRECISION,

    CONSTRAINT "Limit_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Reading" (
    "id" BIGSERIAL NOT NULL,
    "stationId" UUID NOT NULL,
    "sensorId" UUID NOT NULL,
    "parameterId" INTEGER NOT NULL,
    "measuredAt" TIMESTAMPTZ(6) NOT NULL,
    "value" DOUBLE PRECISION NOT NULL,
    "flag" "ReadingFlag" NOT NULL DEFAULT 'OK',
    "receivedAt" TIMESTAMPTZ(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Reading_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Calibration" (
    "id" UUID NOT NULL,
    "sensorId" UUID NOT NULL,
    "parameterId" INTEGER NOT NULL,
    "performedAt" TIMESTAMPTZ(6) NOT NULL,
    "performedById" UUID,
    "referenceValue" DOUBLE PRECISION,
    "sensorBefore" DOUBLE PRECISION,
    "sensorAfter" DOUBLE PRECISION,
    "offset" DOUBLE PRECISION,
    "slope" DOUBLE PRECISION,
    "notes" TEXT,

    CONSTRAINT "Calibration_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Sample" (
    "id" UUID NOT NULL,
    "siteId" UUID NOT NULL,
    "stationId" UUID,
    "source" "SampleSource" NOT NULL,
    "collectedAt" TIMESTAMPTZ(6) NOT NULL,
    "depthM" DECIMAL(6,2),
    "labName" TEXT,
    "collectedById" UUID,
    "notes" TEXT,

    CONSTRAINT "Sample_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "SampleResult" (
    "id" UUID NOT NULL,
    "sampleId" UUID NOT NULL,
    "parameterId" INTEGER NOT NULL,
    "value" DOUBLE PRECISION,
    "qualifier" "ResultQualifier" NOT NULL DEFAULT 'EQUAL',
    "method" TEXT,

    CONSTRAINT "SampleResult_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Alert" (
    "id" UUID NOT NULL,
    "stationId" UUID NOT NULL,
    "parameterId" INTEGER,
    "readingId" BIGINT,
    "severity" "AlertSeverity" NOT NULL,
    "status" "AlertStatus" NOT NULL DEFAULT 'OPEN',
    "message" TEXT NOT NULL,
    "createdAt" TIMESTAMPTZ(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "resolvedAt" TIMESTAMPTZ(6),
    "acknowledgedById" UUID,

    CONSTRAINT "Alert_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "User_email_key" ON "User"("email");

-- CreateIndex
CREATE INDEX "User_organisationId_idx" ON "User"("organisationId");

-- CreateIndex
CREATE UNIQUE INDEX "Site_organisationId_name_key" ON "Site"("organisationId", "name");

-- CreateIndex
CREATE UNIQUE INDEX "Station_siteId_name_key" ON "Station"("siteId", "name");

-- CreateIndex
CREATE UNIQUE INDEX "Sensor_serialNumber_key" ON "Sensor"("serialNumber");

-- CreateIndex
CREATE INDEX "SensorInstallation_stationId_installedAt_idx" ON "SensorInstallation"("stationId", "installedAt");

-- CreateIndex
CREATE INDEX "SensorInstallation_sensorId_installedAt_idx" ON "SensorInstallation"("sensorId", "installedAt");

-- CreateIndex
CREATE UNIQUE INDEX "Parameter_code_key" ON "Parameter"("code");

-- CreateIndex
CREATE UNIQUE INDEX "Standard_name_key" ON "Standard"("name");

-- CreateIndex
CREATE UNIQUE INDEX "Limit_standardId_parameterId_key" ON "Limit"("standardId", "parameterId");

-- CreateIndex
CREATE INDEX "Reading_stationId_parameterId_measuredAt_idx" ON "Reading"("stationId", "parameterId", "measuredAt");

-- CreateIndex
CREATE UNIQUE INDEX "Reading_sensorId_parameterId_measuredAt_key" ON "Reading"("sensorId", "parameterId", "measuredAt");

-- CreateIndex
CREATE INDEX "Calibration_sensorId_parameterId_performedAt_idx" ON "Calibration"("sensorId", "parameterId", "performedAt");

-- CreateIndex
CREATE INDEX "Sample_siteId_collectedAt_idx" ON "Sample"("siteId", "collectedAt");

-- CreateIndex
CREATE UNIQUE INDEX "SampleResult_sampleId_parameterId_key" ON "SampleResult"("sampleId", "parameterId");

-- CreateIndex
CREATE INDEX "Alert_stationId_status_createdAt_idx" ON "Alert"("stationId", "status", "createdAt");

-- AddForeignKey
ALTER TABLE "User" ADD CONSTRAINT "User_organisationId_fkey" FOREIGN KEY ("organisationId") REFERENCES "Organisation"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Site" ADD CONSTRAINT "Site_organisationId_fkey" FOREIGN KEY ("organisationId") REFERENCES "Organisation"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Station" ADD CONSTRAINT "Station_siteId_fkey" FOREIGN KEY ("siteId") REFERENCES "Site"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "SensorInstallation" ADD CONSTRAINT "SensorInstallation_sensorId_fkey" FOREIGN KEY ("sensorId") REFERENCES "Sensor"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "SensorInstallation" ADD CONSTRAINT "SensorInstallation_stationId_fkey" FOREIGN KEY ("stationId") REFERENCES "Station"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Limit" ADD CONSTRAINT "Limit_standardId_fkey" FOREIGN KEY ("standardId") REFERENCES "Standard"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Limit" ADD CONSTRAINT "Limit_parameterId_fkey" FOREIGN KEY ("parameterId") REFERENCES "Parameter"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Reading" ADD CONSTRAINT "Reading_stationId_fkey" FOREIGN KEY ("stationId") REFERENCES "Station"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Reading" ADD CONSTRAINT "Reading_sensorId_fkey" FOREIGN KEY ("sensorId") REFERENCES "Sensor"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Reading" ADD CONSTRAINT "Reading_parameterId_fkey" FOREIGN KEY ("parameterId") REFERENCES "Parameter"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Calibration" ADD CONSTRAINT "Calibration_sensorId_fkey" FOREIGN KEY ("sensorId") REFERENCES "Sensor"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Calibration" ADD CONSTRAINT "Calibration_parameterId_fkey" FOREIGN KEY ("parameterId") REFERENCES "Parameter"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Calibration" ADD CONSTRAINT "Calibration_performedById_fkey" FOREIGN KEY ("performedById") REFERENCES "User"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Sample" ADD CONSTRAINT "Sample_siteId_fkey" FOREIGN KEY ("siteId") REFERENCES "Site"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Sample" ADD CONSTRAINT "Sample_stationId_fkey" FOREIGN KEY ("stationId") REFERENCES "Station"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Sample" ADD CONSTRAINT "Sample_collectedById_fkey" FOREIGN KEY ("collectedById") REFERENCES "User"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "SampleResult" ADD CONSTRAINT "SampleResult_sampleId_fkey" FOREIGN KEY ("sampleId") REFERENCES "Sample"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "SampleResult" ADD CONSTRAINT "SampleResult_parameterId_fkey" FOREIGN KEY ("parameterId") REFERENCES "Parameter"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Alert" ADD CONSTRAINT "Alert_stationId_fkey" FOREIGN KEY ("stationId") REFERENCES "Station"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Alert" ADD CONSTRAINT "Alert_parameterId_fkey" FOREIGN KEY ("parameterId") REFERENCES "Parameter"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Alert" ADD CONSTRAINT "Alert_readingId_fkey" FOREIGN KEY ("readingId") REFERENCES "Reading"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Alert" ADD CONSTRAINT "Alert_acknowledgedById_fkey" FOREIGN KEY ("acknowledgedById") REFERENCES "User"("id") ON DELETE SET NULL ON UPDATE CASCADE;
