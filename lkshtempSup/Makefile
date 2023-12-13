TOP=..
include $(TOP)/configure/CONFIG
#=======================================

# Install .dbd and .db files
# db and proto for 332
DB += lksh332.db 
DATA += lksh332.proto

# db and proto for 372
DB += lakeshore372.db
DATA += lakeshore372.proto lakeshore372.db

# db and proto add for 336
DB += $(patsubst ../%, %, $(wildcard ../*.template))
DB += lakeshore336.db
DATA += ls336.proto

#db and proto and cpp install for 340
DB += Lakeshore340.db
DB += Lakeshore340_channel.db
DATA += Lakeshore340.proto

LIBRARY_IOC += Lakeshore340
DBD += Lakeshore340.dbd

ifeq ($(findstring 10.0,$(VCVERSION)),)
GTESTPROD_HOST+= runner
runner_INC += lakeshore340excitations.h
runner_LIBS += $(EPICS_BASE_IOC_LIBS) asyn
runner_LIBS += asyn utilities
runner_LIBS += asubFunctions
runner_SRCS += lakeshore340excitations.c lakeshore340excitationsTests.cpp
GTESTS += runner
endif

Lakeshore340_DBD += asyn.dbd
Lakeshore340_DBD += aSubFunctions.dbd

Lakeshore340_SRCS += lakeshore340excitations.c

Lakeshore340_LIBS += $(EPICS_BASE_IOC_LIBS)
Lakeshore340_LIBS += asyn utilities
Lakeshore340_LIBS += asubFunctions

#=======================================
include $(TOP)/configure/RULES
