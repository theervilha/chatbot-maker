import requests

class FlowExtractor:
    USER_MESSAGE = 'user-message'
    BOT_MESSAGE = 'bot-message'
    IMPORT_BLOCK = 'import-block'
    FIELDS = [USER_MESSAGE, BOT_MESSAGE, IMPORT_BLOCK]

    def __init__(self, figmaUrl, figmaToken):
        self.figmaUrl = figmaUrl
        self.figmaToken = figmaToken

    def getFigmaData(self):
        fileKey = self.figmaUrl.split("file/")[1].split("/")[0]
        urlAPI = f"https://api.figma.com/v1/files/{fileKey}"
        headers = {'X-FIGMA-TOKEN': self.figmaToken}
        self.figmaData = requests.get(urlAPI, headers=headers).json()
        self.TITLE_PROJECT = self.figmaData['name']
        return self.figmaData

    def getBotDataForEachFlow(self):
        page = self.getPageWithFlows()

        getComponentValue = {
            self.USER_MESSAGE: self.getUserMessage,
            self.BOT_MESSAGE: self.getBotMessage,
            self.IMPORT_BLOCK: self.getImportBlock,
        }
        self.flows = {}
        for flow in page['children']:
            self.flows[flow['name']] = {
                self.USER_MESSAGE: [],
                self.BOT_MESSAGE: [],
                self.IMPORT_BLOCK: [],
            }
            self.messages = []
            self.indexToInsertBlock = 0

            self.components = flow['children']
            for self.i, component in enumerate(self.components):
                componentValue = getComponentValue[component['name']](component)
                self.flows[flow['name']][component['name']].append(componentValue)

            self.flows[flow['name']][self.BOT_MESSAGE] = list(filter(lambda msg: msg != None, self.flows[flow['name']][self.BOT_MESSAGE]))

    def getPageWithFlows(self, pageName='Flows'):
        pages = self.figmaData['document']['children']
        return next(filter(lambda page: page['name'] == pageName, pages), None)

    def getUserMessage(self, component):
        self.indexToInsertBlock += 1
        return component['children'][0]['characters'].lower()

    def getBotMessage(self, component):
        message = component['children'][0]['characters']
        try:
            nextElement = self.components[self.i+1]
        except IndexError:
            if self.messages == []:
                return [message]
            return self.messages
        if nextElement['name'] == self.BOT_MESSAGE:
            nextMessage = nextElement['children'][0]['characters']
            if self.messages == []:
                self.messages.extend([message, nextMessage])
            else:   
                self.messages.append(nextMessage)
        else:
            if self.messages == []:
                return [message]
            
            auxiliarVariable = self.messages
            self.messages = []
            return auxiliarVariable

    def getImportBlock(self, component):
        blockName = component['children'][1]['children'][0]['characters']
        block = {'name': blockName, 'index': self.indexToInsertBlock}
        self.indexToInsertBlock += 1
        return block

    def insertBlockValues(self):
        for flowName, flowValue in self.flows.items():
            self.insertBlockIn(flowValue)

    def insertBlockIn(self, flow):
        appendToFlow = {
            self.USER_MESSAGE: self.appendField,
            self.BOT_MESSAGE: self.appendMessage,
            self.IMPORT_BLOCK: self.appendField,
        }
        self.blocks = flow[self.IMPORT_BLOCK]
        if self.blocks != []:
            self.indexToAppend = self.blocks[0]['index']
            for self.i, self.block in enumerate(self.blocks):
                self.blockFlow = self.flows[self.block['name']]
                blocksInBlocks = self.blockFlow[self.IMPORT_BLOCK]
                if blocksInBlocks != []:
                    self.insertBlockIn(self.blockFlow)

                for self.field in self.FIELDS:
                    blockFieldValue = self.blockFlow[self.field]
                    appendToFlow[self.field](flow, blockFieldValue)

                self.indexToAppend = self.getNextIndexToAppendTheNextBlock()

    def appendField(self, flow, blockValue):
        flow[self.field] = flow[self.field][:self.indexToAppend] + blockValue + flow[self.field][self.indexToAppend:]

    def appendMessage(self, flow, blockValue):
        self.blockUserMessages = self.blockFlow[self.USER_MESSAGE]
        if len(self.blockUserMessages) > 0:
            self.appendField(flow, blockValue)
        else:
            msgUntilIndexConcatened = flow[self.BOT_MESSAGE][:self.indexToAppend][-1] + blockValue[0]
            flow[self.BOT_MESSAGE] = flow[self.BOT_MESSAGE][:self.indexToAppend-1] + [msgUntilIndexConcatened] + flow[self.BOT_MESSAGE][self.indexToAppend:]

    def getNextIndexToAppendTheNextBlock(self):
        userMsgsOfBlock = self.blockFlow[self.USER_MESSAGE]
        deltaUserMsgs = len(userMsgsOfBlock) - 1
        distanceOfNextBlock = self.blocks[self.i+1]['index'] - self.block['index'] if (self.i < len(self.blocks)-1) else 0
        return self.indexToAppend + distanceOfNextBlock + deltaUserMsgs

    def replaceToBeforeFlows(self):
        flowsBeforeReplaced = {key: value for key, value in self.flows.items()}
        self.newFlows = {}
        
        for self.flow in self.flows.keys():
            self.beforeFlows = self.flow.split(" / ")
            lastPath = self.beforeFlows[-1]
            self.newFlows[lastPath] = {self.USER_MESSAGE: [], self.BOT_MESSAGE: [], self.IMPORT_BLOCK: []}
            for self.i in range(len(self.beforeFlows)):
                before = ' / '.join(self.beforeFlows[:self.i+1])
                self.before = flowsBeforeReplaced[before]

                [self.newFlows[lastPath][field].extend(self.before[field]) for field in self.FIELDS]
                
        #self.flows = self.newFlows